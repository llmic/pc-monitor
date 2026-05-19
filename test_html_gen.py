import sys
sys.stdout.reconfigure(encoding='utf-8')

from collector import DataCollector
from generator import HTMLGenerator

# Collect data
collector = DataCollector()
data = collector.collect_all()

# Add required fields
data['computer_name'] = '测试电脑'
data['avatar'] = ''
data['cached_avatar'] = None
data['shutdown_timeout'] = 600
data['max_history'] = 10
data['max_metrics_history'] = 5
data['history_windows'] = []
data['browser_tabs'] = []

# Check bilibili windows
print('=== Windows with bilibili info ===')
count = 0
for w in data['windows']:
    if w.get('bilibili'):
        count += 1
        print(f"[{count}] Title: {w['title']}")
        print(f"  Bilibili: {w['bilibili']}")
        print()
print(f"Total bilibili windows: {count}")

# Generate HTML
generator = HTMLGenerator()
html = generator.generate(data)

# Check if bilibili card is in HTML
if 'Watching Bilibili' in html:
    print('✅ Bilibili card is present in HTML!')
else:
    print('❌ Bilibili card is NOT present in HTML')

# Save HTML
generator.save(html, 'test_output.html')
print('Saved to test_output.html')
