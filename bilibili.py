import re
import requests
import json
import os
from html import unescape

BV_CACHE_FILE = 'data/bv_cache.json'

def load_bv_cache():
    if os.path.exists(BV_CACHE_FILE):
        with open(BV_CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_bv_cache(cache):
    os.makedirs('data', exist_ok=True)
    with open(BV_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def extract_bv_info(title):
    """Extract BV ID from title or URL, handling ? and other parameters."""
    # Pattern to match BV followed by exactly 10 characters (letters and digits)
    # Match BV followed by 10 chars, optionally followed by ? or other chars
    bv_pattern = r'BV([0-9A-Za-z]{10})'
    match = re.search(bv_pattern, title)
    if match:
        bv_id = match.group(0)
        return {
            'bv_id': bv_id,
            'url': f'https://www.bilibili.com/video/{bv_id}/'
        }
    return None

def clean_html_tags(text):
    """Remove HTML tags from text."""
    if text:
        text = unescape(text)
        text = re.sub(r'<[^>]+>', '', text)
    return text

def search_bilibili_video(keyword):
    """Search for a video on Bilibili by keyword."""
    try:
        url = f'https://api.bilibili.com/x/web-interface/search/all/v2?keyword={requests.utils.quote(keyword)}&page=1&limit=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://search.bilibili.com'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                result = data.get('data', {}).get('result', [])
                for item in result:
                    if item.get('result_type') == 'video':
                        videos = item.get('data', [])
                        if videos:
                            video = videos[0]
                            bv_id = video.get('bvid')
                            if bv_id:
                                cover = video.get('pic', '')
                                # Fix relative URL
                                if cover and cover.startswith('//'):
                                    cover = 'https:' + cover
                                
                                duration = video.get('duration', 0)
                                # Convert duration to MM:SS format
                                duration = format_duration(duration)
                                
                                # Get author information
                                author = video.get('author', '')
                                
                                # Get view count, danmaku count, and publish date
                                view_count = video.get('play', 0)
                                danmaku_count = video.get('video_review', 0)
                                pubdate = video.get('pubdate', 0)
                                
                                return {
                                    'bv_id': bv_id,
                                    'url': f'https://www.bilibili.com/video/{bv_id}/',
                                    'title': clean_html_tags(video.get('title', '')),
                                    'cover': cover,
                                    'duration': duration,
                                    'author': author,
                                    'view_count': view_count,
                                    'view_count_formatted': format_number(view_count),
                                    'danmaku_count': danmaku_count,
                                    'danmaku_count_formatted': format_number(danmaku_count),
                                    'pubdate': format_date(pubdate),
                                    'like_count': video.get('like', 0),
                                    'like_count_formatted': format_number(video.get('like', 0))
                                }
    except Exception:
        pass
    return None

def format_number(num):
    """Format numbers to readable format (e.g., 123456 -> 12.3万)."""
    if num >= 100000000:
        return f"{num / 100000000:.2f}亿"
    elif num >= 10000:
        return f"{num / 10000:.1f}万"
    else:
        return str(num)

def format_date(timestamp):
    """Convert Unix timestamp to readable date format."""
    try:
        from datetime import datetime
        if isinstance(timestamp, int):
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except Exception:
        pass
    return ''

def fetch_bilibili_video_detail(bv_id):
    """Fetch detailed video information including duration, author, view count, danmaku, and publish date."""
    try:
        url = f'https://api.bilibili.com/x/web-interface/view?bvid={bv_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                video = data['data']
                cover = video.get('pic', '')
                # Fix relative URL
                if cover and cover.startswith('//'):
                    cover = 'https:' + cover
                
                # Get duration - for multi-part videos, use first part duration
                pages = video.get('pages', [])
                if pages:
                    duration = pages[0].get('duration', video.get('duration', 0))
                else:
                    duration = video.get('duration', 0)
                # Convert duration to MM:SS format
                if isinstance(duration, int):
                    duration = format_duration(duration)
                
                # Get author information
                author = video.get('owner', {}).get('name', '')
                
                # Get stat information (view count, danmaku, like, etc.)
                stat = video.get('stat', {})
                view_count = stat.get('view', 0)
                danmaku_count = stat.get('danmaku', 0)
                like_count = stat.get('like', 0)
                pubdate = video.get('pubdate', 0)
                
                return {
                    'bv_id': bv_id,
                    'url': f'https://www.bilibili.com/video/{bv_id}/',
                    'title': video.get('title', ''),
                    'cover': cover,
                    'duration': duration,
                    'author': author,
                    'view_count': view_count,
                    'view_count_formatted': format_number(view_count),
                    'danmaku_count': danmaku_count,
                    'danmaku_count_formatted': format_number(danmaku_count),
                    'pubdate': format_date(pubdate),
                    'like_count': like_count,
                    'like_count_formatted': format_number(like_count)
                }
    except Exception:
        pass
    return None

def format_duration(duration):
    """Convert duration to MM:SS format."""
    if isinstance(duration, int):
        # duration is in seconds
        hours = duration // 3600
        mins = (duration % 3600) // 60
        secs = duration % 60
        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"
    elif isinstance(duration, str):
        # Already in format like "HH:MM:SS" or "MM:SS"
        parts = duration.split(':')
        if len(parts) == 3:
            # HH:MM:SS - already formatted
            return duration
        elif len(parts) == 2:
            # MM:SS - ensure leading zeros
            mins = int(parts[0])
            secs = int(parts[1])
            return f"{mins:02d}:{secs:02d}"
        elif len(parts) == 1:
            # Just seconds
            secs = int(parts[0])
            mins = secs // 60
            secs = secs % 60
            return f"{mins:02d}:{secs:02d}"
    return str(duration)

def fetch_bilibili_title(bv_id):
    """Fetch video title by BV ID - compatible with main.py."""
    detail = fetch_bilibili_video_detail(bv_id)
    if detail:
        return detail.get('title', '')
    return None

def get_bilibili_info(title):
    """Get bilibili video info from window title, with fallback to search."""
    # First try to extract BV from title
    bv_info = extract_bv_info(title)
    if bv_info:
        detail = fetch_bilibili_video_detail(bv_info['bv_id'])
        if detail:
            return detail
        return bv_info
    
    # If no BV found, try to extract title and search
    # Clean up title to get the actual video title
    clean_title = title
    # Remove common suffixes
    for suffix in ['_哔哩哔哩_bilibili', '_bilibili', '- 哔哩哔哩', '- bilibili', '_哔哩哔哩', ' - 弹幕视频网']:
        if clean_title.endswith(suffix):
            clean_title = clean_title[:-len(suffix)].strip()
    
    # Try searching if we have a meaningful title
    if clean_title and len(clean_title) > 3:
        search_result = search_bilibili_video(clean_title)
        if search_result:
            return search_result
    
    return None