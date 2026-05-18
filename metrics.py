import json
import os
from datetime import datetime
from collections import deque

METRICS_FILE = 'data/metrics_history.json'
MAX_HISTORY_POINTS = 5

def load_metrics_history():
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'cpu': [], 'memory': [], 'timestamps': []}

def save_metrics_history(history):
    os.makedirs('data', exist_ok=True)
    with open(METRICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

class MetricsHistory:
    def __init__(self, max_points=MAX_HISTORY_POINTS):
        self.max_points = max_points
        self.history = load_metrics_history()
        
        # Ensure we have empty lists if keys are missing
        if 'cpu' not in self.history:
            self.history['cpu'] = []
        if 'memory' not in self.history:
            self.history['memory'] = []
        if 'timestamps' not in self.history:
            self.history['timestamps'] = []
    
    def add_data(self, cpu_percent, memory_percent):
        timestamp = datetime.now().isoformat()
        
        self.history['cpu'].append(cpu_percent)
        self.history['memory'].append(memory_percent)
        self.history['timestamps'].append(timestamp)
        
        # Keep only the last max_points
        if len(self.history['cpu']) > self.max_points:
            self.history['cpu'] = self.history['cpu'][-self.max_points:]
            self.history['memory'] = self.history['memory'][-self.max_points:]
            self.history['timestamps'] = self.history['timestamps'][-self.max_points:]
        
        save_metrics_history(self.history)
    
    def get_history(self):
        return self.history
    
    def get_labels(self):
        labels = []
        for ts in self.history['timestamps']:
            try:
                dt = datetime.fromisoformat(ts)
                labels.append(dt.strftime('%H:%M:%S'))
            except Exception:
                labels.append('')
        return labels
