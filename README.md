# PC Monitor

Real-time computer monitoring system with music detection, browser tracking, and system performance metrics.

## Features

- **System Monitoring**: Real-time CPU, Memory, Disk, and Network metrics
- **Music Detection**: Detects NetEase Cloud Music playback with lyrics display
- **Browser Tracking**: Tracks active browser windows and URLs
- **Bilibili Integration**: Monitors Bilibili video viewing with cover images
- **Window History**: Tracks application usage history
- **Auto Screenshots**: Captures screenshots of active windows (privacy-protected)
- **Real-time Updates**: Automatic data refresh at configurable intervals
- **Responsive Dashboard**: Beautiful Bootstrap-based UI

## Project Structure

```
pc-monitor/
├── main.py               # Main entry point
├── generator.py          # HTML generator with Jinja2 templates
├── collector.py          # Data collection module
├── history.py            # Window history management
├── metrics.py            # System metrics tracking
├── music.py              # NetEase Cloud Music integration
├── bilibili.py           # Bilibili video integration
├── templates/            # Jinja2 HTML templates
│   └── index.html       # Main dashboard template
├── static/               # Static assets
│   ├── css/
│   │   └── style.css    # Custom stylesheets
│   └── js/
│       └── main.js      # Client-side JavaScript
├── data/                 # Data cache
│   └── .gitkeep
├── screenshots/          # Screenshot storage
└── index.html            # Generated dashboard (not tracked)
```

## Installation

### Prerequisites

- Python 3.8+
- Windows OS (required for pywin32)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

- `jinja2` - Template engine
- `psutil` - System monitoring
- `pywin32` - Windows API access
- `requests` - HTTP requests
- `uiautomation` - UI automation for browser URL capture
- `Pillow` - Image processing

## Usage

### Run the Monitor

```bash
python main.py
```

### Configuration

Modify `main.py` to adjust settings:

```python
COLLECTION_INTERVAL = 300       # Update interval in seconds
SCREENSHOT_ENABLED = True       # Enable auto-screenshots
DEPLOY_TO_GITHUB = False        # Auto-deploy to GitHub Pages
```

### Dashboard Features

1. **Status Card**: Shows system health and last update time
2. **Performance Charts**: CPU and memory usage trends
3. **Active Windows**: Currently active applications
4. **Music Card**: Current playing song with lyrics
5. **Bilibili Card**: Currently watching video
6. **Window History**: Recent application usage

## Development

### Modify Templates

- **HTML Structure**: Edit `templates/index.html`
- **CSS Styles**: Edit `static/css/style.css`
- **JavaScript**: Edit `static/js/main.js`
- **Python Logic**: Edit respective modules

### Testing

Run individual components:

```bash
# Test music detection
python music.py

# Test Bilibili integration
python bilibili.py
```

## Git Tracking

The `.gitignore` file excludes:
- Generated files (`index.html`)
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Data cache (`data/*.json`)
- Screenshots (`screenshots/`)
- Edge profile (`ms_profile/`)

## License

MIT License

## Acknowledgments

- Bootstrap 5.3.0 for UI components
- Chart.js 4.4.0 for performance charts
- Font Awesome icons
- Bilibili API for video information
- NetEase Cloud Music API for lyrics