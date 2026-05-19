import sys
sys.stdout.reconfigure(encoding='utf-8')

from music import get_music_info
from generator import HTMLGenerator

print("=== Testing Music Card Generation with Simulated Data ===")

# Simulate a NetEase Cloud Music window title
test_title = "Payphone - Maroon 5/Wiz Khalifa - 网易云音乐"
print(f"Testing with title: {test_title}")
print()

# Get music info
music_info = get_music_info(test_title)
print("=== Music Info from API ===")
if music_info:
    print(f"Song: {music_info.get('song')}")
    print(f"Artist: {music_info.get('artist')}")
    print(f"Cover URL: {music_info.get('cover_url')}")
    print(f"Song URL: {music_info.get('song_url')}")
    print(f"Colors: {music_info.get('colors')}")
    print(f"Total Duration: {music_info.get('total_time_str')}")
else:
    print("No music info found")

print()

# Create mock data for HTML generation
mock_data = {
    'windows': [
        {
            'title': test_title,
            'music': music_info
        }
    ],
    'active_window': test_title,
    'system_info': {
        'cpu': [10, 20, 15, 5],
        'memory': {'percent': 45},
        'disk': {'percent': 60},
        'network': {'upload_speed': 100, 'download_speed': 500}
    },
    'screenshot': 'screenshots/test.png',
    'screenshot_reason': 'test',
    'screenshot_message': 'Test screenshot',
    'timestamp': '2024-01-01T00:00:00',
    'avatar': None,
    'cached_avatar': None,
    'browser_tabs': []
}

# Generate HTML
generator = HTMLGenerator()
html = generator.generate(mock_data)
print("=== Checking Music Card in HTML ===")

# Check if music card is present
if '<div class="card music-card' in html:
    print("✓ Music card is present in HTML!")
    
    # Check if cover URL is included
    if music_info and music_info.get('cover_url'):
        if music_info['cover_url'] in html:
            print("✓ Cover image URL is included!")
        else:
            print("✗ Cover image URL not found in HTML")
    
    # Check if song URL is included
    if music_info and music_info.get('song_url'):
        if music_info['song_url'] in html:
            print("✓ Song URL is included in link!")
        else:
            print("✗ Song URL not found in HTML")
    
    # Check if playing icon is shown instead of cover
    if '<i class="bi bi-music-note text-white"' in html and music_info.get('cover_url'):
        print("✗ Error: Showing icon instead of cover image!")
    else:
        print("✓ Correctly showing cover image (not icon)")
else:
    print("✗ Music card not found in HTML")

# Save test output
with open('test_music_output.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\nSaved to test_music_output.html")

# Show snippet of music card
print("\n=== Music Card HTML Snippet ===")
start = html.find('<div class="card music-card')
if start != -1:
    end = html.find('</div>', start) + 6
    print(html[start:end][:1500])
