from collector import DataCollector
import sys

# Set stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

collector = DataCollector()
data = collector.collect_all()
windows = data['windows']

print('Total windows:', len(windows))
print('--- All Windows ---')
for w in windows:
    title = w['title']
    process = w.get('process', '')
    is_browser = 'browser' in w
    has_bilibili = 'bilibili' in w
    
    # Check if title contains bilibili keywords
    has_bilibili_title = 'bilibili' in title.lower() or '哔哩哔哩' in title
    
    try:
        print(f"Title: {title}")
    except:
        print(f"Title: [Unicode error]")
        
    print(f"  Process: {process}")
    print(f"  Is Browser: {is_browser}")
    print(f"  Has Bilibili in title: {has_bilibili_title}")
    print(f"  Has Bilibili data: {has_bilibili}")
    if has_bilibili:
        print(f"  Bilibili: {w['bilibili']}")
    print()
