# PC Monitor

Real-time computer monitoring system with music detection, browser tracking, and system performance metrics.

## Project Structure

```
pc-monitor/
├── generator.py          # Main Python generator (loads templates)
├── templates/           # Jinja2 HTML templates
│   └── index.html     # Main HTML template
├── static/             # Static assets
│   ├── css/
│   │   └── style.css  # Stylesheets
│   └── js/
│       └── main.js     # JavaScript code
├── data/              # Data cache
│   └── music_cache.json
├── music.py            # Music detection module
└── index.html          # Generated HTML output
```

## Usage

### Generate HTML

```python
import generator

gen = generator.HTMLGenerator()
html = gen.generate({
    'current_time': '2024-01-15 10:30:00',
    'windows': [...],
    'system_info': {...},
    # ... other data
})

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

### Modify Templates

- **HTML**: Edit `templates/index.html`
- **CSS**: Edit `static/css/style.css`
- **JavaScript**: Edit `static/js/main.js`
- **Python**: Edit `generator.py`

## File Separation

The project now uses a modular structure:

- `generator.py` contains only Python code and template rendering logic
- `templates/index.html` contains the HTML structure with Jinja2 tags
- `static/css/style.css` contains all CSS styles
- `static/js/main.js` contains all JavaScript code

This separation makes it easier to:
- Maintain code independently
- Track changes with Git
- Reuse assets across multiple templates
- Collaborate with team members

## Git Tracking

The `.gitignore` file excludes:
- Generated files (`index.html`, `generator_backup.py`)
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Data cache files (`data/*.json`)

## Features

- Real-time system monitoring (CPU, Memory, Disk, Network)
- Music detection and lyrics display
- Browser window tracking
- Bilibili video monitoring
- Responsive design
- Status card with health indicators
- Performance charts

## Dependencies

- Python 3.7+
- Jinja2
- pywin32 (for Windows API access)
- Bootstrap 5.3.0
- Chart.js 4.4.0