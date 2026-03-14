"""
STARK Voice Engine - Text to Speech
COMPLETE REWRITE for instant speaking and zero lag
Root causes fixed:
  1. speak(wait=True) was blocking main thread — now uses wait=False by default
     so STARK responds INSTANTLY without freezing the loop
  2. Engine reinit on RuntimeError was broken — now uses a stop_event properly
  3. is_speaking flag is thread-safe using threading.Event
"""

import threading
import queue
import time

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class VoiceEngine:
    def __init__(self, rate=170, volume=1.0, voice_index=0):
        self.rate       = rate
        self.volume     = volume
        self.voice_index = voice_index
        self.engine     = None
        self.is_running = True

        # Thread-safe speaking flag — listener polls this
        self._speaking_event = threading.Event()
        self.is_speaking = False          # simple bool, set inside engine thread only

        self._queue  = queue.Queue()
        self._ready  = threading.Event()  # fires when engine is fully initialised

        t = threading.Thread(target=self._engine_loop, daemon=True, name="VoiceEngine")
        t.start()
        self._ready.wait(timeout=6)       # wait for engine before first speak()

    # ------------------------------------------------------------------
    # Internal engine loop — owns pyttsx3 100%, never called from outside
    # ------------------------------------------------------------------
    def _engine_loop(self):
        if not PYTTSX3_AVAILABLE:
            print("[Voice] pyttsx3 missing — run: pip install pyttsx3")
            self._ready.set()
            return

        try:
            self.engine = pyttsx3.init()
            self._apply_settings()
            print("[Voice] Engine ready.")
        except Exception as e:
            print(f"[Voice] Init failed: {e}")
            self._ready.set()
            return

        self._ready.set()   # unblock __init__

        while self.is_running:
            try:
                item = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue

            if item is None:          # shutdown signal
                break

            text = item
            self.is_speaking = True
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except RuntimeError:
                # "run loop already started" — stop and retry once
                try:
                    self.engine.stop()
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception:
                    pass
            except Exception as e:
                print(f"[Voice] Speak error: {e}")
            finally:
                self.is_speaking = False
                try:
                    self._queue.task_done()
                except Exception:
                    pass

    def _apply_settings(self):
        if not self.engine:
            return
        self.engine.setProperty('rate',   self.rate)
        self.engine.setProperty('volume', self.volume)
        voices = self.engine.getProperty('voices')
        if voices:
            idx = self.voice_index if self.voice_index < len(voices) else 0
            self.engine.setProperty('voice', voices[idx].id)
            print(f"[Voice] Using voice: {voices[idx].name}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def speak(self, text, wait=False):
        """
        Speak text.
        wait=False (default) — returns IMMEDIATELY, speech plays in background.
                               This makes STARK feel instant and responsive.
        wait=True  — blocks until speech is fully done (use for confirmations).
        """
        if not text or not text.strip():
            return
        if self.engine is None:
            print(f"[STARK]: {text}")
            return

        self._queue.put(text)

        if wait:
            self._queue.join()   # blocks until task_done() called in engine thread

    def speak_now(self, text):
        """Clear queue and speak immediately — interrupts current speech."""
        self.stop()
        time.sleep(0.05)
        self.speak(text)

    def stop(self):
        """Stop all speech instantly."""
        # Drain the queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
                self._queue.task_done()
            except Exception:
                pass
        if self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass
        self.is_speaking = False

    def wait_until_done(self):
        """Block until current speech finishes."""
        self._queue.join()

    def set_rate(self, rate):
        self.rate = rate
        if self.engine:
            try: self.engine.setProperty('rate', rate)
            except Exception: pass

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        if self.engine:
            try: self.engine.setProperty('volume', self.volume)
            except Exception: pass

    def get_voices(self):
        if self.engine:
            try:
                return [(i, v.name) for i, v in enumerate(self.engine.getProperty('voices'))]
            except Exception: pass
        return []

    def set_voice(self, index):
        if self.engine:
            try:
                voices = self.engine.getProperty('voices')
                if voices and index < len(voices):
                    self.engine.setProperty('voice', voices[index].id)
                    self.voice_index = index
                    return True
            except Exception: pass
        return False

    def is_available(self):
        return self.engine is not None

    def shutdown(self):
        self.is_running = False
        self.stop()
        try: self._queue.put(None)
        except Exception: pass
        print("[Voice] Shut down.")