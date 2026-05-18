import re
import requests
import json
import os

MUSIC_CACHE_FILE = 'data/music_cache.json'

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

def parse_netease_music_title(title):
    """Parse NetEase Cloud Music window title to extract song info."""
    # 网易云音乐窗口标题格式："歌曲名 - 歌手 - 网易云音乐"
    patterns = [
        r'^(.+?)\s*[-–—]\s*([^-–—]+?)\s*[-–—]\s*网易云音乐',
        r'^(.+?)\s*-\s*([^-]+?)\s*-\s*网易云音乐',
        r'^(.+?)\s*[-–—]\s*网易云音乐'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, title)
        if match:
            if len(match.groups()) == 2:
                return {
                    'song': match.group(1).strip(),
                    'artist': match.group(2).strip(),
                    'player': '网易云音乐'
                }
            else:
                return {
                    'song': match.group(1).strip(),
                    'artist': None,
                    'player': '网易云音乐'
                }
    return None

def fetch_lyrics(song_name, artist_name=None):
    """Fetch lyrics for a song using NetEase Cloud Music API."""
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
                    lyrics = fetch_lyrics_by_id(song_id)
                    if lyrics:
                        cache[cache_key] = lyrics
                        save_music_cache(cache)
                        return lyrics
                    
                    break
    
    except Exception:
        pass
    
    return None

def fetch_lyrics_by_id(song_id):
    """Fetch lyrics by song ID."""
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
            if lyrics:
                return lyrics.strip()
    except Exception:
        pass
    return None

def get_music_info(title):
    """Get music info from window title."""
    netease_info = parse_netease_music_title(title)
    if netease_info:
        song = netease_info['song']
        artist = netease_info['artist']
        lyrics = fetch_lyrics(song, artist)
        if lyrics:
            netease_info['lyrics'] = lyrics
        return netease_info
    return None
