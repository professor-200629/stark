"""
STARK Browser Controller - Web and Media Control
YouTube, Spotify, Netflix, Prime Video, Hotstar
"""

import time
import webbrowser
import subprocess

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
try:
    from utils import safe_type as _safe_type
except ImportError:
    def _safe_type(text):
        try:
            import pyautogui
            pyautogui.typewrite(text, interval=0.05)
        except Exception:
            pass


class BrowserController:
    """Control browsers and streaming platforms"""

    def __init__(self):
        self.is_youtube_open = False
        self.current_site = None
        self.current_video = None
        print("[Browser] Controller initialized.")

    # ========== YOUTUBE ==========

    def open_youtube(self) -> str:
        webbrowser.open("https://www.youtube.com")
        self.is_youtube_open = True
        self.current_site = "youtube"
        return "Sir, YouTube is open."

    def youtube_search(self, query: str) -> str:
        if not query:
            return "Sir, what should I search on YouTube?"

        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.is_youtube_open = True
        self.current_site = "youtube"
        self.current_video = query

        if PYAUTOGUI_AVAILABLE:
            time.sleep(5)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            pyautogui.press('escape')
            time.sleep(0.2)
            for _ in range(4):
                pyautogui.press('tab')
                time.sleep(0.15)
            pyautogui.press('enter')
            time.sleep(1)

        return f"Sir, playing '{query}' on YouTube."

    def youtube_skip_ad(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            # Try different methods to skip ads
            # Method 1: Press 'tab' several times and 'enter'
            for _ in range(3):
                pyautogui.press('tab')
                time.sleep(0.1)
            pyautogui.press('enter')
            
            # Method 2: Some browsers/players support 'shift' + 'n' to skip
            # but that might skip the whole video. 
            
            # Method 3: Try clicking where the skip button usually is
            # (Requires screen coordinates which are hard to predict)
            
        return "Sir, I've attempted to skip the advertisement for you."

    def youtube_pause(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('k') # 'k' is the universal pause/play shortcut on YouTube
        return "Sir, playback has been paused."

    def youtube_resume(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('k')
        return "Sir, playback has been resumed."

    def youtube_next(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('shift', 'n')
        return "Sir, next video."

    def youtube_previous(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('shift', 'p')
        return "Sir, previous video."

    def youtube_fullscreen(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('f')
        return "Sir, fullscreen toggled."

    def youtube_seek(self, seconds: int) -> str:
        if PYAUTOGUI_AVAILABLE:
            if seconds > 0:
                for _ in range(abs(seconds) // 5):
                    pyautogui.press('right')
            else:
                for _ in range(abs(seconds) // 5):
                    pyautogui.press('left')
        return f"Sir, seeked {seconds} seconds."

    def youtube_captions(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('c')
        return "Sir, captions toggled."

    def youtube_speed_up(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('shift', '.')
        return "Sir, playback speed increased."

    def youtube_speed_down(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('shift', ',')
        return "Sir, playback speed decreased."

    # ========== SPOTIFY ==========

    def open_spotify(self) -> str:
        try:
            subprocess.Popen("spotify", shell=True)
            return "Sir, Spotify is opening."
        except Exception:
            webbrowser.open("https://open.spotify.com")
            return "Sir, Spotify web is open."

    def search_spotify(self, song: str) -> str:
        if not song:
            return self.open_spotify()

        try:
            subprocess.Popen("spotify", shell=True)
            time.sleep(3)

            if PYAUTOGUI_AVAILABLE:
                pyautogui.hotkey('ctrl', 'k')
                time.sleep(0.8)
                _safe_type(song)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(0.8)
                pyautogui.press('enter')

            return f"Sir, playing '{song}' on Spotify."
        except Exception:
            webbrowser.open(f"https://open.spotify.com/search/{song.replace(' ', '%20')}")
            return f"Sir, searching '{song}' on Spotify web."

    # ========== STREAMING ==========

    def open_netflix(self) -> str:
        webbrowser.open("https://www.netflix.com")
        self.current_site = "netflix"
        return "Sir, Netflix is open."

    def open_prime_video(self) -> str:
        webbrowser.open("https://www.primevideo.com")
        self.current_site = "prime"
        return "Sir, Prime Video is open."

    def open_hotstar(self) -> str:
        webbrowser.open("https://www.hotstar.com")
        self.current_site = "hotstar"
        return "Sir, JioHotstar is open."

    # ========== VOLUME ==========

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

    def volume_mute(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumemute')
        return "Sir, mute toggled."

    # ========== GENERAL BROWSER ==========

    def open_website(self, url: str) -> str:
        """Open any website by URL"""
        if not url.startswith("http"):
            url = f"https://{url}"
        webbrowser.open(url)
        self.current_site = url
        return f"Sir, opened {url}"

    def google_search(self, query: str) -> str:
        """Search Google for a query"""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.current_site = "google"
        return f"Sir, searching Google for '{query}'."

    def open_url(self, url: str) -> str:
        if not url.startswith('http'):
            url = 'https://' + url
        webbrowser.open(url)
        return f"Sir, opened {url}"

    def search_web(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Sir, searching for '{query}'"

    def close_browser(self):
        """Close the browser using Alt+F4"""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.keyDown('alt')
            pyautogui.keyDown('f4')
            pyautogui.keyUp('f4')
            pyautogui.keyUp('alt')
        self.is_youtube_open = False
        self.current_site = None
        self.current_video = None
        return "Sir, browser closed."

    def close_tab(self):
        """Close current browser tab using Ctrl+W"""
        if PYAUTOGUI_AVAILABLE:
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('w')
            pyautogui.keyUp('w')
            pyautogui.keyUp('ctrl')
        return "Sir, tab closed."

    # ========== MEDIA KEYS ==========

    def media_play_pause(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('playpause')
        return "Sir, play/pause."

    def media_next_track(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('nexttrack')
        return "Sir, next track."

    def media_previous_track(self) -> str:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('prevtrack')
        return "Sir, previous track."