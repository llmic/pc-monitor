# PC Monitor - 实时计算机监控系统

> 一个集成监控与自动部署功能的Python脚本，用于实时收集和展示计算机系统状态信息。

---

## 项目概述

PC Monitor 是一款基于Python的计算机监控系统，能够实时收集系统运行数据并生成可视化的监控面板。系统支持自动部署到GitHub Pages，实现远程访问监控数据。

## 核心功能

- **系统指标监控**
  - CPU 使用率实时追踪
  - 内存使用情况监控
  - 磁盘空间状态检测
  - 网络活动监控

- **窗口与浏览器监控**
  - 活动窗口标题记录
  - 浏览器标签页监控
  - 应用使用时长统计

- **多媒体监控**
  - 当前播放音乐信息展示
  - 歌词同步显示
  - Bilibili 直播状态监控

- **自动部署**
  - 定时自动生成监控面板
  - 自动推送到GitHub Pages
  - 截图自动上传与管理

- **可视化界面**
  - 简洁的白色主题设计
  - 实时状态指示灯
  - 系统指标图表展示
  - 响应式布局设计

## 技术栈

| 分类 | 技术 |
|------|------|
| 编程语言 | Python 3.8+ |
| 前端框架 | Bootstrap 5 |
| 图表库 | Chart.js |
| 部署方式 | GitHub Pages |
| 自动化 | GitHub Actions |

## 环境要求

### 操作系统
- Windows 10/11（推荐）
- Linux（部分功能受限）
- macOS（部分功能受限）

### Python 版本
- Python 3.8 或更高版本

### 依赖库
```plaintext
psutil>=5.9.0
pywin32>=306 (Windows)
Pillow>=9.0.0
requests>=2.28.0
beautifulsoup4>=4.11.0
```

## 安装指南

### 1. 克隆项目
```bash
git clone https://github.com/llmic/pc-monitor.git
cd pc-monitor
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置Git（可选）
如果需要自动部署功能，请配置Git：
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 4. 配置GitHub Pages（可选）
在GitHub仓库设置中：
- 进入 Settings → Pages
- 选择 gh-pages 分支作为源
- 保存配置

## 使用说明

### 基本运行

```bash
python main.py
```

### 配置参数

在 `main.py` 中可修改以下配置：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| COLLECTION_INTERVAL | 数据收集间隔（秒） | 180 |
| OUTPUT_FILE | 输出HTML文件名 | index.html |
| GIT_PUSH_ENABLED | 是否启用自动推送 | True |
| DATA_DIR | 数据文件目录 | data |
| SCREENSHOT_DIR | 截图保存目录 | screenshots |

### 手动生成监控面板

```bash
# 仅生成HTML，不推送
python main.py --no-push
```

### 访问监控面板

部署成功后，通过以下地址访问：
```
https://your-username.github.io/pc-monitor/
示例：https://llmic.github.io/pc-monitor/
```

## 项目结构

```
pc-monitor/
├── main.py              # 主入口脚本
├── collector.py         # 数据收集模块
├── generator.py         # HTML生成模块
├── metrics.py           # 指标历史管理
├── history.py           # 历史记录管理
├── music.py             # 音乐监控模块
├── bilibili.py          # Bilibili监控模块
├── requirements.txt     # 依赖列表
├── index.html           # 生成的监控面板
├── screenshots/         # 截图存储目录
├── data/                # 数据文件目录
└── .github/
    └── workflows/
        └── deploy.yml   # GitHub Actions部署配置
```

## 常见问题

### Q: 监控面板无法显示实时时间？

A: 请检查浏览器控制台是否有JavaScript错误。确保`currentTimeDisplay`元素存在且`updateStatus`函数正常执行。

### Q: 自动部署失败？

A: 请检查：
1. GitHub仓库的Actions权限是否开启
2. `gh-pages`分支是否存在
3. 部署工作流日志中的具体错误信息

### Q: 截图无法显示？

A: 请检查截图目录是否存在，以及CDN配置是否正确。可在`main.py`中修改`SCREENSHOT_CDN_URL`。

### Q: 音乐信息不显示？

A: 该功能依赖特定的音乐播放器API，目前支持部分主流播放器。请确保音乐播放器正在运行。

## 注意事项

1. **隐私保护**：本系统仅在本地收集数据，不会上传敏感信息。但生成的HTML页面可能包含窗口标题等信息，请谨慎分享。

2. **系统资源**：建议将数据收集间隔设置为180秒以上，避免过度占用系统资源。

3. **网络访问**：首次运行需要网络连接以获取头像和其他资源。

4. **管理员权限**：部分系统指标可能需要管理员权限才能获取完整信息。

## 开发说明

### 添加新的监控模块

1. 在项目目录下创建新的模块文件
2. 实现数据收集逻辑
3. 在 `collector.py` 中集成新模块
4. 在 `generator.py` 中添加展示逻辑

### 自定义界面样式

修改 `generator.py` 中的HTML模板部分，可自定义：
- 颜色主题
- 布局结构
- 显示内容

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 项目地址：https://github.com/llmic/pc-monitor
- 提交Issue：https://github.com/llmic/pc-monitor/issues

---

*项目持续更新中，欢迎贡献代码！*
