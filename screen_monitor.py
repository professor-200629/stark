"""
STARK Screen Monitor - Real-time Screen Reading
Live screen monitoring without taking screenshots
"""

import threading
import time
import re
from typing import Optional, Callable

try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class ScreenMonitor:
    """Real-time screen monitoring for STARK"""

    def __init__(self):
        self.is_monitoring = False
        self.current_screen_text = ""
        self.last_capture_time = 0
        self.capture_interval = config.SCREEN_MONITOR_INTERVAL
        self.monitor_thread = None
        self.on_content_change = None
        self.previous_text = ""

        if TESSERACT_AVAILABLE and hasattr(config, 'TESSERACT_PATH'):
            try:
                pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
            except Exception:
                pass

        self.mss_instance = None
        print("[ScreenMonitor] Initialized.")

    def start_monitoring(self):
        if self.is_monitoring:
            return

        self.is_monitoring = True

        if MSS_AVAILABLE:
            try:
                self.mss_instance = mss.mss()
            except Exception:
                pass

        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("[ScreenMonitor] Started real-time monitoring.")

    def _monitor_loop(self):
        while self.is_monitoring:
            try:
                current_time = time.time()

                if current_time - self.last_capture_time >= self.capture_interval:
                    text = self._capture_screen_text()

                    if text and text != self.previous_text:
                        self.previous_text = self.current_screen_text
                        self.current_screen_text = text

                        if self.on_content_change:
                            self.on_content_change(text)

                    self.last_capture_time = current_time

                time.sleep(0.5)

            except Exception as e:
                print(f"[ScreenMonitor] Error: {e}")
                time.sleep(1)

    def _capture_screen_text(self) -> str:
        if MSS_AVAILABLE and TESSERACT_AVAILABLE:
            try:
                text = self._ocr_capture()
                if text:
                    return text
            except Exception:
                pass

        return ""

    def _ocr_capture(self) -> str:
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)

                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

                text = pytesseract.image_to_string(img)
                return text.strip()

        except Exception as e:
            print(f"[ScreenMonitor] OCR error: {e}")
            return ""

    def read_screen_now(self) -> str:
        text = self._capture_screen_text()
        if text:
            return text

        if PYAUTOGUI_AVAILABLE:
            try:
                text = self._clipboard_capture()
                if text:
                    return text
            except Exception:
                pass

        return ""

    def _clipboard_capture(self) -> str:
        try:
            old_clipboard = ""
            try:
                old_clipboard = pyperclip.paste()
            except Exception:
                pass

            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)

            text = pyperclip.paste()

            try:
                pyperclip.copy(old_clipboard)
            except Exception:
                pass

            pyautogui.press('escape')

            return text if text != old_clipboard else ""

        except Exception:
            return ""

    def get_current_content(self) -> str:
        return self.current_screen_text

    def find_text_on_screen(self, search_text: str) -> bool:
        if search_text.lower() in self.current_screen_text.lower():
            return True

        text = self.read_screen_now()
        return search_text.lower() in text.lower()

    def get_code_from_screen(self) -> str:
        text = self.current_screen_text or self.read_screen_now()

        code_pattern = r'(def\s+\w+|class\s+\w+|function\s+\w+|import\s+\w+|const\s+\w+|let\s+\w+)'

        if re.search(code_pattern, text):
            return text

        return text

    def set_capture_interval(self, seconds: int):
        self.capture_interval = max(1, seconds)

    def stop_monitoring(self):
        self.is_monitoring = False

        if self.mss_instance:
            try:
                self.mss_instance.close()
            except Exception:
                pass

        print("[ScreenMonitor] Stopped.")


class CodeWatcher:
    """Watches for code on screen and provides real-time feedback"""

    def __init__(self, screen_monitor: ScreenMonitor):
        self.screen_monitor = screen_monitor
        self.is_watching = False
        self.on_error_detected = None
        self.last_code = ""

    def start_watching(self):
        self.is_watching = True
        self.screen_monitor.on_content_change = self._on_screen_change
        print("[CodeWatcher] Started watching for code.")

    def _on_screen_change(self, new_text: str):
        if not self.is_watching:
            return

        if self._is_code(new_text):
            self._analyze_code(new_text)

    def _is_code(self, text: str) -> bool:
        code_indicators = [
            r'def\s+\w+', r'function\s+\w+', r'class\s+\w+',
            r'import\s+\w+', r'const\s+\w+', r'let\s+\w+',
            r'print\s*\(', r'console\.log', r'return\s+',
        ]

        for pattern in code_indicators:
            if re.search(pattern, text):
                return True

        return False

    def _analyze_code(self, code: str):
        if code == self.last_code:
            return

        self.last_code = code

        errors = []

        if 'print ' in code and 'print(' not in code:
            errors.append("Possible Python 2 print statement (missing parentheses)")

        if code.count('(') != code.count(')'):
            errors.append("Unmatched parentheses detected")

        if code.count('[') != code.count(']'):
            errors.append("Unmatched brackets detected")

        if code.count('{') != code.count('}'):
            errors.append("Unmatched braces detected")

        if errors and self.on_error_detected:
            self.on_error_detected(errors)

    def stop_watching(self):
        self.is_watching = False
        self.screen_monitor.on_content_change = None
        print("[CodeWatcher] Stopped.")