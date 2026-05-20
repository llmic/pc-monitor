import win32gui
import re
import requests
import uiautomation as auto

# ======================================
# 全局配置
# ======================================
WINDOWS_LIST = []
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}
# 强规则：BV号正则
BV_REGEX = re.compile(r"BV[0-9a-zA-Z]{10}")
# 强规则：B站关键词
BILI_KEYWORDS = {"bilibili", "哔哩哔哩", "B站"}
# 主流浏览器类名（用于识别浏览器窗口）
BROWSER_CLASSES = {
    "Chrome_WidgetWin_1",    # Google Chrome
    "Edge_WidgetWin_1",      # Microsoft Edge
    "MozillaWindowClass",    # Firefox
    "360SEWindowClass"       # 360浏览器
}

# ======================================
# 1. 获取浏览器当前网址（核心新增）
# ======================================
def get_browser_url(hwnd: int) -> str | None:
    """获取Chrome/Edge/Firefox浏览器的当前网址"""
    try:
        window = auto.ControlFromHandle(hwnd)
        if window.ClassName in ["Chrome_WidgetWin_1", "Edge_WidgetWin_1"]:
            # Chrome / Edge
            address_bar = window.EditControl(AccessKey='Address')
            return address_bar.GetValuePattern().Value.strip()
        elif window.ClassName == "MozillaWindowClass":
            # Firefox
            address_bar = window.EditControl(Name="地址栏")
            return address_bar.GetValuePattern().Value.strip()
    except:
        return None
    return None

# ======================================
# 2. 枚举所有窗口（新增URL字段）
# ======================================
def get_window_info(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd).strip()
        window_class = win32gui.GetClassName(hwnd)
        if window_title:
            # 判断是否为浏览器，获取URL
            url = get_browser_url(hwnd) if window_class in BROWSER_CLASSES else None
            WINDOWS_LIST.append({
                "hwnd": hwnd,
                "title": window_title,
                "class_name": window_class,
                "url": url  # 新增：浏览器网址
            })

def enum_all_windows():
    global WINDOWS_LIST
    WINDOWS_LIST.clear()
    win32gui.EnumWindows(get_window_info, None)
    return WINDOWS_LIST

# ======================================
# 3. 双来源提取BV号（标题 + URL，优先级：URL > 标题）
# ======================================
def extract_bv(title: str, url: str = None) -> str | None:
    """优先从URL提取BV，再从标题提取，强格式校验"""
    # 1. 优先从浏览器URL提取（最准确）
    if url:
        match = BV_REGEX.search(url)
        if match:
            return match.group()
    # 2. 从窗口标题提取
    match = BV_REGEX.search(title)
    return match.group() if match else None

# ======================================
# 4. B站API解析
# ======================================
def get_bilibili_video_info(bv: str) -> dict | None:
    try:
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
        resp = requests.get(url, headers=HEADERS, timeout=5)
        data = resp.json()
        if data.get("code") == 0:
            info = data["data"]
            return {
                "bv号": bv,
                "视频标题": info["title"],
                "UP主": info["owner"]["name"],
                "播放量": info["stat"]["view"],
                "视频链接": f"https://www.bilibili.com/video/{bv}",
            }
        return None
    except:
        return None

# ======================================
# 5. 强匹配B站窗口
# ======================================
def get_bilibili_windows():
    all_windows = enum_all_windows()
    result = []
    for win in all_windows:
        title = win["title"]
        url = win["url"]
        hwnd = win["hwnd"]

        # 强规则1：标题/URL包含B站关键词
        is_bili = any(key in title for key in BILI_KEYWORDS)
        if url:
            is_bili = is_bili or ("bilibili.com" in url)
        if not is_bili:
            continue

        # 强规则2：提取BV号
        bv = extract_bv(title, url)
        if not bv:
            continue

        # 强规则3：API校验成功
        video_info = get_bilibili_video_info(bv)
        if not video_info:
            continue

        result.append({
            "窗口句柄": hwnd,
            "窗口标题": title,
            "浏览器URL": url,
            "视频信息": video_info
        })
    return result

# ======================================
# 主运行：先打印所有窗口（含URL），再打印B站结果
# ======================================
if __name__ == "__main__":
    # 1. 输出【所有窗口 + 浏览器网址】
    print("=" * 80)
    print("📋 系统所有打开的窗口（含浏览器URL）")
    print("=" * 80)
    all_windows = enum_all_windows()
    for idx, win in enumerate(all_windows, 1):
        url_info = f" | 网址：{win['url']}" if win['url'] else ""
        print(f"[{idx}] 句柄：{win['hwnd']} | 类名：{win['class_name']} | 标题：{win['title']}{url_info}")

    # 2. 输出【B站匹配结果】
    print("\n" + "=" * 80)
    print("🎯 B站视频窗口匹配结果（标题+URL双校验）")
    print("=" * 80)
    bili_result = get_bilibili_windows()

    if not bili_result:
        print("未找到匹配的 Bilibili 视频窗口")
    else:
        for i, item in enumerate(bili_result, 1):
            print(f"\n===== 匹配成功 {i} =====")
            print(f"窗口句柄：{item['窗口句柄']}")
            print(f"窗口标题：{item['窗口标题']}")
            print(f"打开网址：{item['浏览器URL']}")
            print(f"BV 号：{item['视频信息']['bv号']}")
            print(f"视频标题：{item['视频信息']['视频标题']}")
            print(f"UP 主：{item['视频信息']['UP主']}")
            print(f"播放量：{item['视频信息']['播放量']}")