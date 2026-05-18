# PC Monitor - Real-time Computer Monitoring System

A unified Python application that combines monitoring, data collection, and Git deployment into a single easy-to-use script.

![Demo](https://img.shields.io/badge/Demo-Online-green)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue)

**Live Demo:** [https://llmic.github.io/pc-monitor/](https://llmic.github.io/pc-monitor/)

## Features

- ✅ **System Monitoring**: CPU, memory, disk, network metrics
- ✅ **Window Tracking**: Real-time active window and all open windows
- ✅ **Browser Integration**: Display web page titles and clickable URLs
- ✅ **Screenshot Capture**: Auto-capture active window at intervals
- ✅ **White Theme Interface**: Clean, minimal white background design
- ✅ **Auto-Deployment**: Built-in Git push to GitHub Pages

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

## Access the Dashboard

Your monitoring dashboard will be available at:

```
https://your-username.github.io/your-repo/
```

## Dashboard Features

1. **System Status**: Green/red indicator for update health
2. **Resource Metrics**: CPU, memory, disk, network usage
3. **Screenshot**: Last captured active window
4. **Browser Windows**: Browser tabs with clickable URLs
5. **All Windows**: Complete list of currently open windows
6. **Timeout Alerts**: Warning if update takes too long

## Troubleshooting

- **Git Push Failures**: Ensure your Git is properly configured and you have push access
- **Screenshot Issues**: Check that `Pillow` is installed (`pip install Pillow`)
- **Permission Errors**: Run the script with appropriate system permissions

## License

MIT License - Feel free to use and modify!