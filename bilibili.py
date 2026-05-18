import re
import requests
import json
import os

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
    bv_pattern = r'BV([0-9A-Za-z]{10})'
    match = re.search(bv_pattern, title)
    if match:
        bv_id = match.group(0)
        return {
            'bv_id': bv_id,
            'url': f'https://www.bilibili.com/video/{bv_id}/'
        }
    return None

def fetch_bilibili_title(bv_id):
    cache = load_bv_cache()
    if bv_id in cache:
        return cache[bv_id]

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
                title = data['data']['title']
                cache[bv_id] = title
                save_bv_cache(cache)
                return title
    except Exception:
        pass
    return None

def fetch_bilibili_cover(bv_id):
    """Fetch video cover image URL."""
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
                return data['data'].get('pic', '')
    except Exception:
        pass
    return None

def get_bilibili_info(title):
    bv_info = extract_bv_info(title)
    if bv_info:
        bv_info['title'] = fetch_bilibili_title(bv_info['bv_id'])
        bv_info['cover'] = fetch_bilibili_cover(bv_info['bv_id'])
        return bv_info
    return None