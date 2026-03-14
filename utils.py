"""
STARK Shared Utilities
Common helper functions used across multiple modules
"""

import time

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


def safe_type(text):
    """Type text supporting non-ASCII via clipboard paste fallback.

    Handles Telugu, Hindi, and other non-Latin scripts by falling back
    to clipboard paste when pyautogui.typewrite() cannot handle the chars.
    """
    if not PYAUTOGUI_AVAILABLE:
        return
    try:
        # If pure ASCII, typewrite is fine
        text.encode('ascii')
        pyautogui.typewrite(text, interval=0.03)
    except UnicodeEncodeError:
        # Non-ASCII (Telugu, Hindi, etc.) — use clipboard paste
        if PYPERCLIP_AVAILABLE:
            old = ""
            try:
                old = pyperclip.paste()
            except Exception:
                pass
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            try:
                pyperclip.copy(old)
            except Exception:
                pass
        else:
            pyautogui.typewrite(text, interval=0.03)


def safe_hotkey(*keys):
    """Safely press a keyboard shortcut"""
    if not PYAUTOGUI_AVAILABLE:
        return False
    try:
        pyautogui.hotkey(*keys)
        return True
    except Exception:
        return False


def get_clipboard():
    """Get clipboard content"""
    if not PYPERCLIP_AVAILABLE:
        return ""
    try:
        return pyperclip.paste()
    except Exception:
        return ""


def set_clipboard(text):
    """Set clipboard content"""
    if not PYPERCLIP_AVAILABLE:
        return False
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False