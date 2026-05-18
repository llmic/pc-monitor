import json
import os
from datetime import datetime
from collections import OrderedDict

# Default settings - can be overridden by passing parameters to HistoryManager
DEFAULT_HISTORY_FILE = 'data/history_windows.json'
DEFAULT_MOUSE_FILE = 'data/mouse_actions.json'
DEFAULT_MAX_HISTORY = 30
DEFAULT_MAX_MOUSE_ACTIONS = 50

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

def load_mouse_actions(mouse_file=DEFAULT_MOUSE_FILE):
    if os.path.exists(mouse_file):
        try:
            with open(mouse_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'actions': []}

def save_mouse_actions(mouse_data, mouse_file=DEFAULT_MOUSE_FILE):
    os.makedirs(os.path.dirname(mouse_file) or '.', exist_ok=True)
    with open(mouse_file, 'w', encoding='utf-8') as f:
        json.dump(mouse_data, f, ensure_ascii=False, indent=2)

class HistoryManager:
    def __init__(self, history_file=DEFAULT_HISTORY_FILE, mouse_file=DEFAULT_MOUSE_FILE,
                 max_history=DEFAULT_MAX_HISTORY, max_mouse_actions=DEFAULT_MAX_MOUSE_ACTIONS):
        self.history_file = history_file
        self.mouse_file = mouse_file
        self.max_history = max_history
        self.max_mouse_actions = max_mouse_actions
        self.history = load_history(history_file)
        self.mouse_actions = load_mouse_actions(mouse_file)
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

    def add_mouse_action(self, action):
        self.mouse_actions['actions'].insert(0, {
            'action': action,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.mouse_actions['actions']) > self.max_mouse_actions:
            self.mouse_actions['actions'] = self.mouse_actions['actions'][:self.max_mouse_actions]
        save_mouse_actions(self.mouse_actions, self.mouse_file)

    def get_history_windows(self):
        return self.history['windows']

    def get_mouse_actions(self):
        return self.mouse_actions['actions']

    def get_bilibili_windows(self):
        return [w for w in self.history['windows'] if w.get('bilibili')]

    def update_from_current_windows(self, current_windows):
        for win in current_windows:
            self.add_window(win)