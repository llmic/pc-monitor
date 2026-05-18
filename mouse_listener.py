from pynput import mouse
from datetime import datetime
import threading

class MouseListener:
    def __init__(self, history_manager):
        self.history_manager = history_manager
        self.listener = None
        self.enabled = True

    def on_click(self, x, y, button, pressed):
        if not self.enabled:
            return
        if pressed:
            button_name = str(button).replace('Button.', '')
            action = f"点击 ({button_name}) at ({x}, {y})"
            self.history_manager.add_mouse_action(action)

    def start(self):
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.daemon = True
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def pause(self):
        self.enabled = False

    def resume(self):
        self.enabled = True