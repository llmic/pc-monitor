import re
import requests
import json
import os
import ctypes
import hashlib
from ctypes import wintypes

try:
    import win32gui
    import win32process
    import win32api
    from win32con import PROCESS_ALL_ACCESS
    import pymem
    from PIL import Image
except ImportError:
    win32gui = None
    win32process = None
    win32api = None
    pymem = None
    Image = None

MUSIC_CACHE_FILE = 'data/music_cache.json'
COLORS_CACHE_FILE = 'data/colors_cache.json'

def load_music_cache():
    if os.path.exists(MUSIC_CACHE_FILE):
        try:
            with open(MUSIC_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_music_cache(cache):
    os.makedirs('data', exist_ok=True)
    with open(MUSIC_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def load_colors_cache():
    if os.path.exists(COLORS_CACHE_FILE):
        try:
            with open(COLORS_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_colors_cache(cache):
    os.makedirs('data', exist_ok=True)
    with open(COLORS_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_dominant_colors(image_path=None, num_colors=3):
    """Extract dominant colors from an image file or URL."""
    try:
        if Image is None:
            return None

        if image_path and image_path.startswith(('http://', 'https://')):
            # Add proper headers for NetEase Cloud Music images
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://music.163.com'
            }
            response = requests.get(image_path, headers=headers, timeout=5)
            if response.status_code != 200:
                return None
            img = Image.open(BytesIO(response.content))
        elif image_path and os.path.exists(image_path):
            img = Image.open(image_path)
        else:
            return None

        img = img.convert('RGB')
        img = img.resize((100, 100))

        pixels = list(img.getdata())

        from collections import Counter
        color_counts = Counter(pixels)

        common_colors = color_counts.most_common(num_colors)

        colors = []
        for color, count in common_colors:
            r, g, b = color
            colors.append(f'#{r:02x}{g:02x}{b:02x}')

        if colors:
            primary = colors[0]
            secondary = colors[1] if len(colors) > 1 else colors[0]
            return {
                'primary': primary,
                'secondary': secondary,
                'gradient': f'linear-gradient(135deg, {primary} 0%, {secondary} 100%)'
            }
    except Exception:
        pass
    return None

def get_song_color_from_cache(song_name, artist_name=None):
    """Get cached color for a song."""
    cache = load_colors_cache()
    cache_key = f"{song_name}_{artist_name or 'unknown'}"

    if cache_key in cache:
        return cache[cache_key]

    return None

def save_song_colors(song_name, artist_name, colors):
    """Save color data for a song to cache."""
    cache = load_colors_cache()
    cache_key = f"{song_name}_{artist_name or 'unknown'}"

    cache[cache_key] = colors
    save_colors_cache(cache)

def get_contrasting_text_color(hex_color):
    """Calculate contrasting text color (black or white) based on background color."""
    try:
        hex_color = hex_color.lstrip('#')
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

def get_predefined_color_palette():
    """Return a white-based color palette for songs without album art."""
    palettes = [
        {'primary': '#ffffff', 'secondary': '#f8f9fa', 'gradient': 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)'},
        {'primary': '#ffffff', 'secondary': '#e9ecef', 'gradient': 'linear-gradient(135deg, #ffffff 0%, #e9ecef 100%)'},
        {'primary': '#ffffff', 'secondary': '#dee2e6', 'gradient': 'linear-gradient(135deg, #ffffff 0%, #dee2e6 100%)'},
        {'primary': '#f8f9fa', 'secondary': '#ffffff', 'gradient': 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)'},
        {'primary': '#ffffff', 'secondary': '#ffffff', 'gradient': 'linear-gradient(135deg, #ffffff 0%, #ffffff 100%)'},
    ]
    return palettes

def get_color_for_song(song_name, artist_name=None, cover_url=None):
    """Get color palette for a song, extracting from cover if available."""
    cached = get_song_color_from_cache(song_name, artist_name)
    if cached:
        return cached

    colors = None
    if cover_url:
        try:
            colors = get_dominant_colors(image_path=cover_url)
        except Exception:
            pass

    if colors:
        save_song_colors(song_name, artist_name, colors)
        return colors

    palettes = get_predefined_color_palette()
    hash_input = f"{song_name}_{artist_name or ''}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    palette = palettes[hash_value % len(palettes)]

    save_song_colors(song_name, artist_name, palette)
    return palette

def get_current_lyric():
    """Get real-time lyrics directly from NetEase Cloud Music desktop lyric window."""
    if win32gui is None:
        return None

    lyric_classes = ["OrpheusDesktopLyricWidget", "DesktopLyrics"]

    def callback(handle, extra):
        class_name = win32gui.GetClassName(handle)
        if class_name in lyric_classes:
            lyric_text = win32gui.GetWindowText(handle)
            if lyric_text.strip():
                extra["lyric"] = lyric_text
        return True

    result = {}
    win32gui.EnumWindows(callback, result)
    return result.get("lyric")

def is_desktop_lyrics_active():
    """Check if NetEase Cloud Music desktop lyrics is currently active."""
    if win32gui is None:
        return False

    lyric_classes = ["OrpheusDesktopLyricWidget", "DesktopLyrics"]

    def callback(handle, extra):
        class_name = win32gui.GetClassName(handle)
        if class_name in lyric_classes:
            extra["active"] = True
            extra["class"] = class_name
        return True

    result = {}
    win32gui.EnumWindows(callback, result)
    return result.get("active", False)

def get_memory_lyrics():
    """Get real-time lyrics by reading NetEase Cloud Music process memory."""
    if pymem is None:
        return None

    try:
        import win32gui

        lyric_classes = ["OrpheusDesktopLyricWidget", "DesktopLyrics"]

        def find_lyric_window(handle, extra):
            class_name = win32gui.GetClassName(handle)
            if class_name in lyric_classes:
                extra["handle"] = handle
            return True

        result = {}
        win32gui.EnumWindows(find_lyric_window, result)

        if not result.get("handle"):
            return None

        hwnd = result["handle"]
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        hProcess = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

        kernel32 = ctypes.windll.kernel32
        ReadProcessMemory = kernel32.ReadProcessMemory
        ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
        ReadProcessMemory.restype = wintypes.BOOL

        try:
            pm = pymem.Pymem(pid)
            cloudmusic_module = None
            for module in pm.list_modules():
                if module.name == "cloudmusic.dll":
                    cloudmusic_module = module.lpBaseOfDll
                    break

            if not cloudmusic_module:
                return None

            base_addr = cloudmusic_module + 0x019D9410
            addr = ctypes.c_ulonglong()
            bytes_read = ctypes.c_size_t()

            if ReadProcessMemory(int(hProcess), ctypes.c_void_p(base_addr), ctypes.byref(addr), 8, ctypes.byref(bytes_read)):
                ret = addr.value + 0xE0
                if ReadProcessMemory(int(hProcess), ctypes.c_void_p(ret), ctypes.byref(addr), 8, ctypes.byref(bytes_read)):
                    ret2 = addr.value + 0x8
                    if ReadProcessMemory(int(hProcess), ctypes.c_void_p(ret2), ctypes.byref(addr), 8, ctypes.byref(bytes_read)):
                        ret3 = addr.value + 0x120
                        if ReadProcessMemory(int(hProcess), ctypes.c_void_p(ret3), ctypes.byref(addr), 8, ctypes.byref(bytes_read)):
                            ret4 = addr.value + 0x8
                            lyrics_addr = ret4

                            lyrics_len = 500
                            raw_bytes = pm.read_bytes(lyrics_addr, lyrics_len)
                            use_bytes = raw_bytes.split(b'\x00\x00')[0]
                            if len(use_bytes) % 2 == 1:
                                use_bytes += b'\x00'

                            try:
                                lyrics = use_bytes.decode('utf-16-le').strip()
                                if lyrics:
                                    return lyrics
                            except UnicodeDecodeError:
                                pass
        finally:
            win32api.CloseHandle(hProcess)

    except Exception:
        pass

    return None

def get_song_info():
    """Get song title and artist from NetEase Cloud Music window title."""
    if win32gui is None:
        return None, None

    def callback(handle, extra):
        title = win32gui.GetWindowText(handle)
        match = re.search(r"(.+?)-(.+?)-网易云音乐", title)
        if match:
            extra["song"] = match.group(1).strip()
            extra["artist"] = match.group(2).strip()
        return True

    info = {}
    win32gui.EnumWindows(callback, info)
    return info.get("song"), info.get("artist")

def parse_netease_music_title(title):
    """Parse NetEase Cloud Music window title to extract song info."""
    if not title:
        return None
    
    # 排除浏览器窗口标题
    browser_keywords = ['microsoft edge', 'chrome', 'firefox', 'safari', 'opera', 'edge', 'browser']
    for keyword in browser_keywords:
        if keyword in title.lower():
            return None

    patterns = [
        r'^(.+?)\s*[-–—]\s*([^-–—]+?)\s*[-–—]\s*网易云音乐',
        r'^(.+?)\s*-\s*([^-]+?)\s*-\s*网易云音乐',
        r'^(.+?)\s*[-–—]\s*网易云音乐',
        r'^(.+?)\s*[-–—]\s*([^\s]+?)$',
        r'^(.+?)\s+-\s+(.+?)$'
    ]

    for pattern in patterns:
        match = re.match(pattern, title)
        if match:
            if len(match.groups()) == 2:
                song = match.group(1).strip()
                artist = match.group(2).strip()
                if song and song != 'No title' and song != 'None':
                    return {
                        'song': song,
                        'artist': artist,
                        'player': '网易云音乐'
                    }
            else:
                song = match.group(1).strip()
                if song and song != 'No title' and song != 'None':
                    return {
                        'song': song,
                        'artist': None,
                        'player': '网易云音乐'
                    }
    return None

def search_song_cover(song_name, artist_name=None):
    """Search for song cover URL using NetEase Cloud Music API."""
    try:
        search_keyword = f"{song_name} {artist_name or ''}"
        search_url = 'https://music.163.com/api/search/get'
        params = {
            's': search_keyword,
            'type': 1,
            'limit': 5
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://music.163.com'
        }

        response = requests.get(search_url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            songs = data.get('result', {}).get('songs', [])

            for song in songs:
                song_name_lower = song_name.lower()
                song_name_match = song.get('name', '').lower()

                if song_name_lower in song_name_match or song_name_match in song_name_lower:
                    if artist_name:
                        artist_match = False
                        for artist in song.get('artists', []):
                            if artist_name.lower() in artist.get('name', '').lower():
                                artist_match = True
                                break
                        if not artist_match:
                            continue

                    song_id = song.get('id')
                    song_detail = get_song_detail(song_id)
                    if song_detail:
                        return song_detail
                    break
    except Exception:
        pass
    return None

def get_song_detail(song_id):
    """Get song details including cover URL and duration."""
    try:
        url = f'https://music.163.com/api/song/detail/?id={song_id}&ids=[{song_id}]'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://music.163.com'
        }

        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            songs = data.get('songs', [])
            if songs:
                song = songs[0]
                album = song.get('album', {})
                return {
                    'song_id': song_id,
                    'title': song.get('name'),
                    'artist': ', '.join([a.get('name', '') for a in song.get('artists', [])]),
                    'album': album.get('name', ''),
                    'cover_url': album.get('picUrl', ''),
                    'duration': song.get('duration', 0)
                }
    except Exception:
        pass
    return None

def parse_lrc_with_timestamps(lrc_text, translation_text=None):
    """Parse LRC format lyrics and extract timestamps, with optional translation."""
    if not lrc_text:
        return []

    lines = lrc_text.strip().split('\n')
    parsed = []
    
    # Parse translation if provided
    translations = {}
    if translation_text:
        trans_lines = translation_text.strip().split('\n')
        for line in trans_lines:
            match = re.match(r'\[(\d+):(\d+)\.(\d+)\](.*)', line)
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                milliseconds = int(match.group(3))
                content = match.group(4).strip()
                if content:
                    total_seconds = minutes * 60 + seconds + milliseconds / 1000.0
                    translations[round(total_seconds, 3)] = content

    for line in lines:
        match = re.match(r'\[(\d+):(\d+)\.(\d+)\](.*)', line)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            milliseconds = int(match.group(3))
            content = match.group(4).strip()

            if content:
                total_seconds = minutes * 60 + seconds + milliseconds / 1000.0
                translation = translations.get(round(total_seconds, 3), None)
                parsed.append({
                    'time': total_seconds,
                    'text': content,
                    'translation': translation
                })

    return parsed

def time_to_seconds(time_str: str) -> int:
    """Convert time string 01:23 to total seconds 83"""
    if not time_str or ":" not in time_str:
        return 0
    try:
        minute, second = time_str.split(":")
        return int(minute) * 60 + int(second)
    except:
        return 0

def get_cloudmusic_progress():
    """
    Get NetEase Cloud Music playback progress from window title
    Returns: (current_sec, total_sec, current_time, total_time, status)
    Example: (83, 225, "01:23", "03:45", "Playing")
    """
    if win32gui is None:
        return 0, 0, "00:00", "00:00", "Not Running"
    
    PLAYER_WINDOW_CLASS = "OrpheusPlayerWidget"
    
    progress_info = {
        "current_sec": 0,
        "total_sec": 0, 
        "current_time": "00:00",
        "total_time": "00:00",
        "status": "Not Playing"
    }
    
    def callback(handle, extra):
        if win32gui.GetClassName(handle) == PLAYER_WINDOW_CLASS:
            window_text = win32gui.GetWindowText(handle)
            match = re.search(r'(\d+:\d+)\s*/\s*(\d+:\d+)', window_text)
            if match:
                current_time = match.group(1)
                total_time = match.group(2)
                current_sec = time_to_seconds(current_time)
                total_sec = time_to_seconds(total_time)
                extra.update({
                    "current_sec": current_sec,
                    "total_sec": total_sec,
                    "current_time": current_time,
                    "total_time": total_time,
                    "status": "Playing" if current_sec > 0 else "Paused"
                })
        return True
    
    result = {}
    win32gui.EnumWindows(callback, result)
    return (
        result.get("current_sec", 0),
        result.get("total_sec", 0),
        result.get("current_time", "00:00"),
        result.get("total_time", "00:00"),
        result.get("status", "Not Running/Not Playing")
    )

def get_current_playback_position():
    """Get current playback position from NetEase Cloud Music window title"""
    current_sec, _, _, _, _ = get_cloudmusic_progress()
    if current_sec > 0:
        return float(current_sec)
    return None

def fetch_lyrics(song_name, artist_name=None):
    """Fetch lyrics for a song using NetEase Cloud Music API, including translation."""
    cache = load_music_cache()
    cache_key = f"{song_name}_{artist_name or 'unknown'}"
    
    if cache_key in cache:
        return cache[cache_key]
    
    try:
        # Search for song
        search_url = 'https://music.163.com/api/search/get'
        params = {
            's': song_name,
            'type': 1,
            'limit': 5
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://music.163.com'
        }
        
        response = requests.get(search_url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            songs = data.get('result', {}).get('songs', [])
            
            for song in songs:
                song_name_lower = song_name.lower()
                song_name_match = song.get('name', '').lower()
                
                # Match song name
                if song_name_lower in song_name_match or song_name_match in song_name_lower:
                    # Check artist match if provided
                    if artist_name:
                        artist_match = False
                        for artist in song.get('artists', []):
                            if artist_name.lower() in artist.get('name', '').lower():
                                artist_match = True
                                break
                        if not artist_match:
                            continue
                    
                    # Get lyrics
                    song_id = song.get('id')
                    lyrics_data = fetch_lyrics_by_id(song_id)
                    if lyrics_data:
                        cache[cache_key] = lyrics_data
                        save_music_cache(cache)
                        return lyrics_data
                    
                    break
    
    except Exception:
        pass
    
    return None

def fetch_lyrics_by_id(song_id):
    """Fetch lyrics by song ID, including translation."""
    try:
        url = f'https://music.163.com/api/song/lyric?id={song_id}&lv=-1&kv=-1&tv=-1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://music.163.com'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get('lrc', {}).get('lyric', '')
            translation = data.get('tlyric', {}).get('lyric', '')
            if lyrics:
                return {
                    'lyrics': lyrics.strip(),
                    'translation': translation.strip() if translation else None
                }
    except Exception:
        pass
    return None

def format_duration(milliseconds):
    """Convert milliseconds to MM:SS format."""
    seconds = int(milliseconds / 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def get_music_info(title):
    """Get music info from window title, with real-time lyrics from desktop lyric window or memory."""
    netease_info = parse_netease_music_title(title)
    if netease_info:
        song = netease_info['song']
        artist = netease_info['artist']

        song_detail = search_song_cover(song, artist)
        if song_detail:
            netease_info['cover_url'] = song_detail.get('cover_url', '')
            netease_info['album'] = song_detail.get('album', '')
            song_id = song_detail.get('song_id')
            if song_id:
                netease_info['song_id'] = song_id
                netease_info['song_url'] = f'https://music.163.com/#/song?id={song_id}'
            
            # Use artist from API if available
            api_artist = song_detail.get('artist')
            if api_artist:
                netease_info['artist'] = api_artist
            
            # Use duration from API if available
            api_duration = song_detail.get('duration', 0)
            if api_duration > 0:
                netease_info['total_duration'] = api_duration / 1000.0
                netease_info['total_time_str'] = format_duration(api_duration)

        colors = get_color_for_song(song, netease_info.get('artist'), netease_info.get('cover_url'))
        netease_info['colors'] = colors

        netease_info['desktop_lyrics_active'] = is_desktop_lyrics_active()

        real_time_lyric = get_current_lyric()
        if real_time_lyric and real_time_lyric != '桌面歌词':
            netease_info['current_lyric'] = real_time_lyric
            netease_info['lyrics'] = real_time_lyric
        else:
            memory_lyric = get_memory_lyrics()
            if memory_lyric:
                netease_info['current_lyric'] = memory_lyric
                netease_info['lyrics'] = memory_lyric
            else:
                lyrics_data = fetch_lyrics(song, netease_info.get('artist'))
                if lyrics_data:
                    if isinstance(lyrics_data, dict):
                        netease_info['lyrics'] = lyrics_data.get('lyrics', '')
                        translation = lyrics_data.get('translation')
                        netease_info['parsed_lyrics'] = parse_lrc_with_timestamps(
                            lyrics_data.get('lyrics', ''), 
                            translation
                        )
                    else:
                        netease_info['lyrics'] = lyrics_data
                        netease_info['parsed_lyrics'] = parse_lrc_with_timestamps(lyrics_data)

        current_sec, total_sec, current_time, total_time, status = get_cloudmusic_progress()
        
        # Use API duration as primary source, fallback to progress info
        if 'total_duration' not in netease_info or netease_info['total_duration'] <= 0:
            netease_info['total_duration'] = float(total_sec) if total_sec > 0 else None
            netease_info['total_time_str'] = total_time if total_time else '00:00'
        
        if 'playback_position' not in netease_info or netease_info['playback_position'] is None:
            netease_info['playback_position'] = float(current_sec) if current_sec > 0 else None
        
        if 'current_time_str' not in netease_info or not netease_info['current_time_str']:
            netease_info['current_time_str'] = current_time if current_time else '00:00'
        
        netease_info['playback_status'] = status

        # Check if song has ended
        if netease_info['total_duration'] and netease_info['playback_position']:
            if netease_info['playback_position'] >= netease_info['total_duration'] - 2:
                netease_info['song_ended'] = True
            else:
                netease_info['song_ended'] = False
        else:
            netease_info['song_ended'] = False

        return netease_info
    return None
