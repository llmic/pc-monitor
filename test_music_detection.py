import sys
import io
import win32process
import psutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')

from music import get_music_info, get_cloudmusic_progress, parse_netease_music_title
import win32gui

print('=' * 60)
print('🎵 音乐检测状态')
print('=' * 60)

# 1. 检查进程是否在运行
print('1. 检查进程状态:')
cloudmusic_running = False
cloudmusic_pids = []
for proc in psutil.process_iter(['name', 'pid']):
    try:
        if 'cloudmusic' in proc.name().lower():
            cloudmusic_running = True
            cloudmusic_pids.append(proc.pid)
            print('   ✅ 网易云音乐进程正在运行:', proc.name(), '(PID:', proc.pid, ')')
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

if not cloudmusic_running:
    print('   ❌ 未找到网易云音乐进程')

# 2. 获取所有属于网易云音乐进程的窗口
print()
print('2. 获取网易云音乐进程的所有窗口:')

def get_windows_for_pids(pids):
    result = []
    def callback(handle, extra):
        _, pid = win32process.GetWindowThreadProcessId(handle)
        if pid in pids:
            title = win32gui.GetWindowText(handle)
            class_name = win32gui.GetClassName(handle)
            is_visible = win32gui.IsWindowVisible(handle)
            result.append({
                'handle': handle,
                'pid': pid,
                'title': title,
                'class': class_name,
                'visible': is_visible
            })
        return True
    win32gui.EnumWindows(callback, None)
    return result

all_cloudmusic_windows = []
if cloudmusic_pids:
    all_cloudmusic_windows = get_windows_for_pids(cloudmusic_pids)
    print('   ✅ 找到', len(all_cloudmusic_windows), '个网易云音乐窗口:')
    for win in all_cloudmusic_windows:
        print('   ---')
        print('   PID:', win['pid'])
        print('   句柄:', win['handle'])
        print('   标题:', repr(win['title']))
        print('   类名:', win['class'])
        print('   可见:', '是' if win['visible'] else '否')
        
        # 尝试解析标题
        if win['title']:
            info = parse_netease_music_title(win['title'])
            if info:
                print('   🎵 解析成功:')
                print('     歌曲:', info.get('song'))
                print('     歌手:', info.get('artist'))
            elif '-' in win['title']:
                print('   ⚠️ 标题包含分隔符但未匹配:', win['title'])

# 3. 获取播放进度
print()
print('=' * 60)
print('📊 播放进度信息')
print('=' * 60)
current_sec, total_sec, current_time, total_time, status = get_cloudmusic_progress()
print('当前时间:', current_time)
print('总时长:', total_time)
print('状态:', status)
print('当前秒数:', current_sec)
print('总秒数:', total_sec)

# 4. 获取完整音乐信息
if all_cloudmusic_windows:
    print()
    print('=' * 60)
    print('🎶 尝试从所有窗口提取音乐信息')
    print('=' * 60)
    for win in all_cloudmusic_windows:
        if win['title']:
            music_info = get_music_info(win['title'])
            if music_info:
                print('✅ 从窗口提取成功:')
                for key, value in music_info.items():
                    print('   ', key, ':', value)
                break
    else:
        print('❌ 无法从任何窗口提取音乐信息')

# 5. 测试桌面歌词读取
print()
print('=' * 60)
print('📝 桌面歌词检测')
print('=' * 60)
from music import get_current_lyric, is_desktop_lyrics_active
print('桌面歌词活跃:', is_desktop_lyrics_active())
lyric = get_current_lyric()
print('当前歌词:', lyric)
