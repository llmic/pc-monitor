import sys
sys.stdout.reconfigure(encoding='utf-8')

from collector import DataCollector
from generator import HTMLGenerator, HTML_TEMPLATE

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

# Debug: Check all windows
print('=== All Windows ===')
for i, w in enumerate(data['windows']):
    has_bilibili = 'bilibili' in w
    print(f"[{i}] Title: {w['title'][:80]}...")
    print(f"  Process: {w.get('process')}")
    print(f"  Has bilibili: {has_bilibili}")
    if has_bilibili:
        print(f"  Bilibili data: {w['bilibili']}")
    print()

# Debug: Check bilibili windows specifically
bilibili_windows = [w for w in data['windows'] if w.get('bilibili')]
print(f'=== Total bilibili windows: {len(bilibili_windows)} ===')

# Generate HTML
generator = HTMLGenerator()
html = generator.generate(data)

# Check if bilibili card is in HTML
if 'Watching Bilibili' in html:
    print('✅ Bilibili card IS present in HTML!')
else:
    print('❌ Bilibili card is NOT present in HTML')
    # Debug: Check if windows variable is being passed correctly
    import jinja2
    template = jinja2.Template(HTML_TEMPLATE)
    # Test with just the bilibili windows
    test_data = {
        'windows': bilibili_windows,
        'computer_name': 'Test',
        'avatar': '',
        'cached_avatar': None,
        'shutdown_timeout': 600,
        'max_history': 10,
        'max_metrics_history': 5,
        'history_windows': [],
        'browser_tabs': [],
        'current_music': None,
        'screenshot': None,
        'cpu_percent': 0,
        'memory_percent': 0,
        'memory_used_gb': '0',
        'memory_total_gb': '0',
        'network_sent': '0',
        'network_recv': '0',
        'cpu_cores': [],
        'metrics_history': [],
        'metrics_labels': [],
        'timestamp': '2024-01-01T00:00:00',
        'browser_windows': [],
        'is_normal_window_active': False,
        'active_normal_window_title': '',
        'is_browser_active': False,
        'active_browser_title': ''
    }
    test_html = template.render(test_data)
    if 'Watching Bilibili' in test_html:
        print('✅ Test with only bilibili windows works!')
    else:
        print('❌ Test with only bilibili windows also fails')

# Save HTML
generator.save(html, 'debug_output.html')
print('Saved to debug_output.html')

# Also print the actual bilibili card section if present
if 'Watching Bilibili' in html:
    start = html.find('Watching Bilibili') - 50
    end = start + 500
    print('\n=== Bilibili Card HTML ===')
    print(html[start:end])
