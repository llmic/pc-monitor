import sys
sys.stdout.reconfigure(encoding='utf-8')

from collector import get_browser_url_from_title, extract_bv_info
from bilibili import get_bilibili_info

# Test the problematic title
title = "【参考信息第602期】取消科长否决权；更新访华美企天团_哔哩哔哩_bilibili - Personal - Microsoft Edge"

print(f"Title: {title}")
print()

# Test extract_bv_info
bv_info = extract_bv_info(title)
print(f"extract_bv_info result: {bv_info}")
print()

# Test get_browser_url_from_title
url = get_browser_url_from_title(title, 'msedge.exe')
print(f"get_browser_url_from_title result: {url}")
print()

# Test get_bilibili_info
bilibili_info = get_bilibili_info(title)
print(f"get_bilibili_info result: {bilibili_info}")
