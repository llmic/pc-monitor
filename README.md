# PC Monitor - Real-time Computer Monitoring System

A unified Python application that combines monitoring, data collection, and Git deployment into a single easy-to-use script.

![Demo](https://img.shields.io/badge/Demo-Online-green)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue)

**Live Demo:** [https://llmic.github.io/pc-monitor/](https://llmic.github.io/pc-monitor/)

## Features

### Core Features
- ✅ **System Monitoring**: CPU, memory, disk, network metrics with history trends
- ✅ **Window Tracking**: Real-time active window and all open windows
- ✅ **Browser Integration**: Display web page titles and clickable URLs
- ✅ **Screenshot Capture**: Auto-capture active window at intervals
- ✅ **White Theme Interface**: Clean, minimal white background design
- ✅ **Auto-Deployment**: Built-in Git push to GitHub Pages

### Extended Features
- ✅ **Bilibili Integration**: Auto-detect Bilibili video playing and display video info (title, cover, duration, author, views, danmaku count)
- ✅ **Music Integration**: Display currently playing NetEase Cloud Music with lyrics
- ✅ **Privacy Protection**: Skip screenshot for privacy windows (WeChat, QQ, Teams, Zoom, etc.)
- ✅ **Performance Trend**: Chart showing last 5 updates of system metrics
- ✅ **Screenshot Management**: Auto-cleanup old screenshots (keep latest 2 of 10)

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your Git repository (if not already configured):
   ```bash
   git init
   git remote add origin https://github.com/your-username/your-repo.git
   ```

3. Enable GitHub Pages in your repository settings (branch: `gh-pages`)

## Usage

### Simple Mode (Recommended)

Just run the unified script:

```bash
python main.py
```

This will:
- Start monitoring your system
- Automatically push updates to GitHub every 90 seconds
- Display the monitoring dashboard in your browser

### Custom Configuration

Edit `main.py` to customize:
- `COLLECTION_INTERVAL = 90`: Change the update interval (seconds)
- `GIT_PUSH_ENABLED = True`: Enable/disable auto-deployment
- `SCREENSHOT_CDN_URL`: Custom screenshot CDN URL

## Access the Dashboard

Your monitoring dashboard will be available at:

```
https://your-username.github.io/your-repo/
```

## Dashboard Features

### 1. Status Card
- **Indicator Light**: Green (normal) → Orange (warning > 2min) → Red (danger > 5min)
- **Last Updated**: Timestamp of last system update
- **Current Time**: Real-time clock (updates every second)
- **Auto-shutdown Warning**: Alert overlay if no update for 10 minutes

### 2. System Metrics
- CPU usage percentage
- Memory usage with available amount
- Disk usage with total/free space
- Network upload/download speed

### 3. Performance Trend Chart
- Line chart showing CPU and memory usage over last 5 updates
- Visual trend analysis

### 4. Active Window
- Current active window title
- Window screenshot (with privacy protection)
- Privacy notice for protected apps (WeChat, QQ, etc.)

### 5. Now Playing (Music)
- Song title and artist
- Album cover image
- Real-time lyrics display
- Lyrics translation support
- Song progress indicator

### 6. Watching Bilibili
- Video title
- Video cover image
- Duration, author, BV ID
- View count, danmaku count, publish date
- Clickable link to video

### 7. All Windows
- Complete list of currently open windows
- Browser tabs with clickable URLs
- Bilibili video windows marked specially

## Privacy Protection

The system automatically skips screenshot capture for the following privacy-sensitive applications:
- WeChat, QQ, WeCom
- Tencent Meeting, WeMeet
- Microsoft Teams, Zoom, Skype
- DingTalk, Feishu (Lark)

When a privacy window is active, a privacy notice is displayed instead of the screenshot.

## Project Structure

```
pc-monitor/
├── main.py              # Main entry point
├── collector.py         # System data collection
├── generator.py         # HTML template generation
├── metrics.py           # Performance metrics tracking
├── bilibili.py          # Bilibili API integration
├── music.py             # NetEase Cloud Music integration
├── history.py           # Window history management
├── requirements.txt     # Python dependencies
├── screenshots/         # Screenshot storage
└── index.html           # Generated dashboard
```

## Troubleshooting

- **Git Push Failures**: Ensure your Git is properly configured and you have push access
- **Screenshot Issues**: Check that `Pillow` is installed (`pip install Pillow`)
- **Permission Errors**: Run the script with appropriate system permissions
- **Bilibili Info Not Showing**: Ensure network access to Bilibili API
- **Music Info Not Showing**: Ensure NetEase Cloud Music is running

## License

MIT License - Feel free to use and modify!
