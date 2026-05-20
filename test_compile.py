# 简单测试模板编译
from jinja2 import Environment
from generator import HTML_TEMPLATE

def contrasting_color(hex_color):
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return '#ffffff'
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return '#000000' if brightness > 0.5 else '#ffffff'
    except:
        return '#ffffff'

def filename_filter(path):
    try:
        return path.split('/')[-1].split('\\')[-1]
    except:
        return path

def truncate_filter(s, length):
    try:
        if len(s) > length:
            return s[:length] + '...'
        return s
    except:
        return s

def strftime_filter(dt_str, format_str):
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime(format_str)
    except:
        return dt_str

def format_time(seconds):
    try:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    except:
        return "00:00"

env = Environment()
env.filters['contrasting_color'] = contrasting_color
env.filters['filename'] = filename_filter
env.filters['truncate'] = truncate_filter
env.filters['strftime'] = strftime_filter
env.filters['format_time'] = format_time

print("Starting template compilation...")
try:
    template = env.from_string(HTML_TEMPLATE)
    print("模板编译成功！")
except Exception as e:
    print(f"模板编译失败: {e}")
    import traceback
    traceback.print_exc()
