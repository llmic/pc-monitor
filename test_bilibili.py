import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collector import DataCollector
from bilibili import extract_bv_info, get_bilibili_info

# Test BV extraction
test_url = 'https://www.bilibili.com/video/BV1zfLc61EUA/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=6198a7ee5cc7ff8d6da472a64f852034'
print("Testing BV extraction from URL...")
bv_info = extract_bv_info(test_url)
print(f"BV Info: {bv_info}")

# Test full bilibili info
print("\nTesting full bilibili info...")
full_info = get_bilibili_info(test_url)
print(f"Full Bilibili Info: {full_info}")

# Test data collection
print("\nTesting data collection...")
collector = DataCollector()
data = collector.collect_all()

print(f"\nWindows found: {len(data.get('windows', []))}")
print(f"Browser tabs: {len(data.get('browser_tabs', []))}")

# Check for bilibili windows
bilibili_windows = [win for win in data.get('windows', []) if win.get('bilibili')]
print(f"\nBilibili windows found: {len(bilibili_windows)}")
for i, win in enumerate(bilibili_windows):
    print(f"\nWindow {i+1}:")
    print(f"  Title: {win.get('title')}")
    print(f"  Bilibili info: {win.get('bilibili')}")

# Check browser tabs for bilibili
browser_tabs = data.get('browser_tabs', [])
bilibili_tabs = [tab for tab in browser_tabs if 'bilibili' in tab.get('url', '').lower()]
print(f"\nBilibili browser tabs found: {len(bilibili_tabs)}")
for i, tab in enumerate(bilibili_tabs):
    print(f"\nTab {i+1}:")
    print(f"  Title: {tab.get('title')}")
    print(f"  URL: {tab.get('url')}")
    print(f"  Domain: {tab.get('domain')}")