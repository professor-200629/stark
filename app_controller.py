"""
STARK App Controller - System and Application Control
"""

import subprocess
import os
import time

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from utils import safe_type as _safe_type
except ImportError:
    def _safe_type(text):
        try:
            import pyautogui
            pyautogui.typewrite(text, interval=0.05)
        except Exception:
            pass


class AppController:
    """Control system applications and functions"""

    def __init__(self):
        self.app_commands = {
            "notepad": "notepad",
            "calculator": "calc",
            "paint": "mspaint",
            "cmd": "cmd",
            "command prompt": "cmd",
            "terminal": "wt",
            "powershell": "powershell",
            "task manager": "taskmgr",
            "file explorer": "explorer",
            "explorer": "explorer",
            "settings": "ms-settings:",
            "control panel": "control",
            "chrome": "start chrome",
            "firefox": "start firefox",
            "edge": "start msedge",
            "vscode": "code",
            "vs code": "code",
            "visual studio": "devenv",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "spotify": "spotify",
            "vlc": "vlc",
            "discord": "discord",
            "zoom": "zoom",
            "teams": "msteams",
            "whatsapp": "whatsapp://",
            "telegram": "telegram://",
            "slack": "slack://",
        }
        print("[AppController] Initialized.")

    def open_app(self, app_name: str) -> str:
        app_lower = app_name.lower().strip()

        for key, cmd in self.app_commands.items():
            if key in app_lower:
                return self._launch_app(key, cmd)

        if "." in app_name and " " not in app_name:
            import webbrowser
            url = app_name if app_name.startswith("http") else f"https://{app_name}"
            webbrowser.open(url)
            return f"Sir, opened {app_name}"

        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.hotkey('win')
                time.sleep(0.5)
                _safe_type(app_name)
                time.sleep(1)
                pyautogui.press('enter')
                return f"Sir, opening {app_name}"
        except Exception:
            pass

        return f"Sir, couldn't find application: {app_name}"

    def _launch_app(self, name: str, command: str) -> str:
        try:
            if command.endswith("://"):
                import webbrowser
                webbrowser.open(command)
            elif command.startswith("ms-"):
                os.system(f"start {command}")
            elif command.startswith("start "):
                os.system(command)
            else:
                subprocess.Popen(command, shell=True)

            return f"Sir, opened {name}"
        except Exception as e:
            return f"Sir, couldn't open {name}: {e}"

    def close_app(self, app_name: str) -> str:
        process_map = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "notepad": "notepad.exe",
            "vscode": "Code.exe",
            "code": "Code.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
            "spotify": "Spotify.exe",
            "discord": "Discord.exe",
            "zoom": "Zoom.exe",
            "vlc": "vlc.exe",
            "telegram": "Telegram.exe",
            "whatsapp": "WhatsApp.exe",
        }

        app_lower = app_name.lower()

        for key, proc in process_map.items():
            if key in app_lower:
                os.system(f"taskkill /f /im {proc}")
                return f"Sir, closed {app_name}"

        os.system(f'taskkill /f /im {app_lower}.exe 2>nul')
        return f"Sir, attempted to close {app_name}"

    # ========== WINDOW MANAGEMENT ==========

    def minimize_window(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('win', 'down')
        return "Sir, minimized window."

    def maximize_window(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('win', 'up')
        return "Sir, maximized window."

    def switch_window(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'tab')
        return "Sir, switched window."

    def close_window(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'f4')
        return "Sir, closed window."

    # ========== SCREENSHOTS ==========

    def screenshot(self, save_path: str = None) -> str:
        if not PYAUTOGUI_AVAILABLE:
            return "Sir, screenshot feature not available."

        if not save_path:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.expanduser(f"~/Desktop/screenshot_{timestamp}.png")

        try:
            pyautogui.screenshot().save(save_path)
            return f"Sir, screenshot saved to {save_path}"
        except Exception as e:
            return f"Sir, couldn't take screenshot: {e}"

    # ========== SYSTEM CONTROL ==========

    def lock_screen(self) -> str:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Sir, screen locked."

    def shutdown_computer(self, delay: int = 60) -> str:
        os.system(f"shutdown /s /t {delay}")
        return f"Sir, computer will shut down in {delay} seconds."

    def restart_computer(self, delay: int = 60) -> str:
        os.system(f"shutdown /r /t {delay}")
        return f"Sir, computer will restart in {delay} seconds."

    def cancel_shutdown(self) -> str:
        os.system("shutdown /a")
        return "Sir, shutdown cancelled."

    def sleep_computer(self) -> str:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Sir, computer going to sleep."

    # ========== SYSTEM INFO ==========

    def get_system_info(self) -> str:
        if not PSUTIL_AVAILABLE:
            return "Sir, system info not available (psutil missing)."

        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/')

            return f"""Sir, system status:
• CPU Usage: {cpu_percent}%
• Memory: {memory.percent}% used ({round(memory.used / (1024**3), 1)} GB / {round(memory.total / (1024**3), 1)} GB)
• Disk: {disk.percent}% used"""
        except Exception:
            return "Sir, couldn't get system info."

    def get_running_apps(self) -> str:
        if not PSUTIL_AVAILABLE:
            return "Sir, process list not available (psutil missing)."

        try:
            processes = []
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name']
                    if name and name not in processes:
                        processes.append(name)
                except Exception:
                    continue

            main_apps = [p for p in processes if not p.lower().startswith(
                ('system', 'svchost', 'runtime', 'csrss', 'lsass', 'wininit', 'services', 'smss')
            )]
            main_apps = sorted(main_apps)[:20]

            return "Sir, running applications:\n" + "\n".join(f"  • {p}" for p in main_apps)
        except Exception:
            return "Sir, couldn't get process list."

    # ========== VOLUME & BRIGHTNESS ==========

    def volume_up(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            for _ in range(3):
                pyautogui.press('volumeup')
        return "Sir, volume increased."

    def volume_down(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            for _ in range(3):
                pyautogui.press('volumedown')
        return "Sir, volume decreased."

    def mute(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumemute')
        return "Sir, mute toggled."

    def brightness_up(self) -> str:
        try:
            import screen_brightness_control as sbc
            current = sbc.get_brightness()[0]
            sbc.set_brightness(min(100, current + 10))
            return "Sir, brightness increased."
        except Exception:
            return "Sir, brightness control not available."

    def brightness_down(self) -> str:
        try:
            import screen_brightness_control as sbc
            current = sbc.get_brightness()[0]
            sbc.set_brightness(max(0, current - 10))
            return "Sir, brightness decreased."
        except Exception:
            return "Sir, brightness control not available."