import json
import os
from datetime import datetime

DEFAULT_HISTORY_FILE = 'data/history_windows.json'
DEFAULT_MAX_HISTORY = 30

def load_history(history_file=DEFAULT_HISTORY_FILE):
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'windows': [], 'last_update': None}

def save_history(history, history_file=DEFAULT_HISTORY_FILE):
    os.makedirs(os.path.dirname(history_file) or '.', exist_ok=True)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

class HistoryManager:
    def __init__(self, history_file=DEFAULT_HISTORY_FILE, max_history=DEFAULT_MAX_HISTORY):
        self.history_file = history_file
        self.max_history = max_history
        self.history = load_history(history_file)
        
        # 确保历史记录数量不超过 max_history
        if len(self.history['windows']) > self.max_history:
            self.history['windows'] = self.history['windows'][:self.max_history]
            save_history(self.history, self.history_file)
        
        self.seen_titles = set(w['title'] for w in self.history['windows'])

    def add_window(self, window_info):
        title = window_info['title']
        if title in self.seen_titles:
            for w in self.history['windows']:
                if w['title'] == title:
                    w['last_seen'] = datetime.now().isoformat()
                    break
        else:
            self.seen_titles.add(title)
            new_entry = {
                'title': title,
                'process': window_info.get('process', 'Unknown'),
                'bilibili': window_info.get('bilibili'),
                'website': window_info.get('website'),
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            }
            self.history['windows'].insert(0, new_entry)
            if len(self.history['windows']) > self.max_history:
                removed = self.history['windows'].pop()
                self.seen_titles.discard(removed['title'])

        self.history['last_update'] = datetime.now().isoformat()
        save_history(self.history, self.history_file)

    def get_history_windows(self):
        return self.history['windows']

    def get_bilibili_windows(self):
        return [w for w in self.history['windows'] if w.get('bilibili')]

    def update_from_current_windows(self, current_windows):
        for win in current_windows:
            self.add_window(win)
