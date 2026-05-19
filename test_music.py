import sys
sys.stdout.reconfigure(encoding='utf-8')

from music import get_music_info, search_song_cover, get_song_detail, parse_netease_music_title

# Test parse_netease_music_title
test_titles = [
    "Payphone - Maroon 5/Wiz Khalifa - 网易云音乐",
    "Kickstart （アウトロ）- BACK-ON",
    "桌面歌词"
]

for title in test_titles:
    print(f"Testing parse_netease_music_title with: {title}")
    result = parse_netease_music_title(title)
    print(f"Result: {result}")
    print()

# Test get_music_info with actual format
print("=== Testing get_music_info ===")
music_info = get_music_info("Payphone - Maroon 5/Wiz Khalifa - 网易云音乐")
if music_info:
    print(f"Song: {music_info.get('song')}")
    print(f"Artist: {music_info.get('artist')}")
    print(f"Cover URL: {music_info.get('cover_url')}")
    print(f"Song URL: {music_info.get('song_url')}")
    print(f"Song Detail Called: {'cover_url' in music_info}")
else:
    print("No music info found")

print()

# Test search_song_cover directly
print("=== search_song_cover result ===")
cover_info = search_song_cover("Payphone", "Maroon 5")
if cover_info:
    print(f"Title: {cover_info.get('title')}")
    print(f"Artist: {cover_info.get('artist')}")
    print(f"Cover URL: {cover_info.get('cover_url')}")
    print(f"Song ID: {cover_info.get('song_id')}")
    print(f"Duration: {cover_info.get('duration')}")
else:
    print("No cover info found")
