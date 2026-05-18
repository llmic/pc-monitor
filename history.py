import json
import os
from datetime import datetime
from collections import OrderedDict

HISTORY_FILE = 'data/history_windows.json'
MOUSE_FILE = 'data/mouse_actions.json'
MAX_HISTORY = 30
MAX_MOUSE_ACTIONS = 50

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'windows': [], 'last_update': None}

def save_history(history):
    os.makedirs('data', exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_mouse_actions():
    if os.path.exists(MOUSE_FILE):
        try:
            with open(MOUSE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'actions': []}

def save_mouse_actions(mouse_data):
    os.makedirs('data', exist_ok=True)
    with open(MOUSE_FILE, 'w', encoding='utf-8') as f:
        json.dump(mouse_data, f, ensure_ascii=False, indent=2)

class HistoryManager:
    def __init__(self):
        self.history = load_history()
        self.mouse_actions = load_mouse_actions()
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
            if len(self.history['windows']) > MAX_HISTORY:
                removed = self.history['windows'].pop()
                self.seen_titles.discard(removed['title'])

        self.history['last_update'] = datetime.now().isoformat()
        save_history(self.history)

    def add_mouse_action(self, action):
        self.mouse_actions['actions'].insert(0, {
            'action': action,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.mouse_actions['actions']) > MAX_MOUSE_ACTIONS:
            self.mouse_actions['actions'] = self.mouse_actions['actions'][:MAX_MOUSE_ACTIONS]
        save_mouse_actions(self.mouse_actions)

    def get_history_windows(self):
        return self.history['windows']

    def get_mouse_actions(self):
        return self.mouse_actions['actions']

    def get_bilibili_windows(self):
        return [w for w in self.history['windows'] if w.get('bilibili')]

    def update_from_current_windows(self, current_windows):
        for win in current_windows:
            self.add_window(win)