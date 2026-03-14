"""
STARK Voice Listener - Speech Recognition
COMPLETE REWRITE for instant, reliable listening
Root causes fixed:
  1. `with self.microphone as source` was opened/closed every loop iteration
     → causes PyAudio hardware reset every cycle = broken/choppy audio
     → FIXED: use listen_in_background() which keeps mic open permanently
  2. No cooldown after STARK speaks — mic picked up echo/reverb
     → FIXED: 0.6s cooldown after is_speaking drops to False
  3. listen_once() was competing with background thread for mic access
     → FIXED: pauses background thread during listen_once()
  4. dynamic_energy_threshold=True was inflating threshold in quiet rooms
     → FIXED: disabled, using fixed calibrated threshold
"""

import threading
import queue
import time

try:
    import speech_recognition as sr
    SR_OK = True
except ImportError:
    SR_OK = False


class VoiceListener:
    def __init__(self, voice_engine=None):
        self.voice_engine   = voice_engine
        self.recognizer     = None
        self.microphone     = None
        self.is_listening   = False
        self.command_queue  = queue.Queue()
        self.last_command   = None
        self._stop_bg       = None          # callable to stop background listener
        self._paused        = False         # True while listen_once() is running
        self._last_spoke_at = 0.0           # timestamp STARK finished speaking

        self._init_recognizer()

    def set_voice_engine(self, ve):
        self.voice_engine = ve

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def _init_recognizer(self):
        if not SR_OK:
            print("[Listener] SpeechRecognition missing.")
            print("[Listener] Run: pip install SpeechRecognition pyaudio")
            return
        try:
            self.recognizer = sr.Recognizer()

            # Fixed threshold — dynamic causes problems in quiet rooms
            self.recognizer.energy_threshold        = 300
            self.recognizer.dynamic_energy_threshold = False   # ✅ FIXED
            self.recognizer.pause_threshold          = 0.6     # faster end-of-phrase detection
            self.recognizer.phrase_threshold         = 0.3
            self.recognizer.non_speaking_duration    = 0.4

            mic_idx = self._find_microphone()
            self.microphone = sr.Microphone(device_index=mic_idx)

            print("[Listener] Calibrating mic...")
            with self.microphone as src:
                self.recognizer.adjust_for_ambient_noise(src, duration=1.5)
            print(f"[Listener] Ready. Threshold={self.recognizer.energy_threshold:.0f}")

        except OSError as e:
            print(f"[Listener] Mic error: {e}")
            print("[Listener] Fix: pip install pipwin && pipwin install pyaudio")
            self.recognizer = self.microphone = None
        except Exception as e:
            print(f"[Listener] Init error: {e}")
            self.recognizer = self.microphone = None

    def _find_microphone(self):
        try:
            names = sr.Microphone.list_microphone_names()
            print(f"[Listener] Mics: {names}")
            for i, n in enumerate(names):
                if any(k in n.lower() for k in ["microphone","mic","input","headset","realtek","audio"]):
                    print(f"[Listener] Selected [{i}]: {n}")
                    return i
        except Exception:
            pass
        print("[Listener] Using default mic.")
        return None

    # ------------------------------------------------------------------
    # Start / Stop
    # ------------------------------------------------------------------
    def start_listening(self):
        if not self.recognizer or not self.microphone:
            print("[Listener] Cannot start — not initialized.")
            return False

        self.is_listening = True

        # ✅ KEY FIX: listen_in_background keeps mic open permanently
        # No hardware reset between phrases — smooth, continuous capture
        self._stop_bg = self.recognizer.listen_in_background(
            self.microphone,
            self._on_audio,
            phrase_time_limit=12
        )
        print("[Listener] Background listening started.")
        return True

    def _on_audio(self, recognizer, audio):
        """Called by background thread every time a phrase is captured."""

        # ── Ignore if paused (listen_once is active) ──
        if self._paused:
            return

        # ── Ignore if STARK is speaking ──
        if self._stark_speaking():
            return

        # ── Cooldown after STARK finishes speaking (prevents echo pickup) ──
        since_spoke = time.time() - self._last_spoke_at
        if since_spoke < 0.7:
            return

        try:
            text = recognizer.recognize_google(audio).lower().strip()
            if text:
                print(f"[Listener] ▶ '{text}'")
                self.command_queue.put(text)
                self.last_command = text
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"[Listener] API error: {e}")

    def stop_listening(self):
        self.is_listening = False
        if self._stop_bg:
            try: self._stop_bg(wait_for_stop=False)
            except Exception: pass
        print("[Listener] Stopped.")

    # ------------------------------------------------------------------
    # Get command
    # ------------------------------------------------------------------
    def get_command(self, timeout=1):
        try:
            return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    # ------------------------------------------------------------------
    # listen_once — for confirmations ("yes/no") after STARK asks something
    # ------------------------------------------------------------------
    def listen_once(self, timeout=6):
        if not self.recognizer or not self.microphone:
            return None

        # Wait for STARK to finish speaking, then add small cooldown
        deadline = time.time() + 4
        while self._stark_speaking():
            if time.time() > deadline: break
            time.sleep(0.05)
        time.sleep(0.4)   # brief gap so mic settles

        # Pause background listener so it doesn't compete
        self._paused = True
        try:
            with self.microphone as src:
                self.recognizer.adjust_for_ambient_noise(src, duration=0.2)
                print("[Listener] Waiting for your response...")
                audio = self.recognizer.listen(src, timeout=timeout, phrase_time_limit=10)

            text = self.recognizer.recognize_google(audio).lower().strip()
            print(f"[Listener] Response: '{text}'")
            return text

        except sr.WaitTimeoutError:
            print("[Listener] No response.")
            return None
        except sr.UnknownValueError:
            print("[Listener] Couldn't understand.")
            return None
        except sr.RequestError as e:
            print(f"[Listener] API error: {e}")
            return None
        except Exception as e:
            print(f"[Listener] listen_once error: {e}")
            return None
        finally:
            self._paused = False   # always unpause background listener

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _stark_speaking(self):
        if self.voice_engine is not None:
            return self.voice_engine.is_speaking
        return False

    def notify_stark_done_speaking(self):
        """Call this right after voice.speak() returns to start cooldown."""
        self._last_spoke_at = time.time()

    def is_available(self):
        return self.recognizer is not None and self.microphone is not None


# ======================================================================
class KeyboardListener:
    """Fallback when microphone is unavailable"""

    def __init__(self, voice_engine=None):
        self.voice_engine  = voice_engine
        self.is_listening  = False
        self.command_queue = queue.Queue()
        self._thread       = None

    def set_voice_engine(self, ve):
        self.voice_engine = ve

    def start_listening(self):
        self.is_listening = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("[Keyboard] Type your commands and press Enter.")

    def _loop(self):
        while self.is_listening:
            try:
                text = input("You: ").strip().lower()
                if text:
                    self.command_queue.put(text)
            except EOFError:
                break
            except Exception as e:
                print(f"[Keyboard] {e}")

    def get_command(self, timeout=1):
        try:
            return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def listen_once(self, timeout=6):
        try:
            return input("You: ").strip().lower()
        except Exception:
            return None

    def stop_listening(self):
        self.is_listening = False

    def notify_stark_done_speaking(self):
        """No-op for keyboard listener (no echo to worry about)."""
        pass

    def is_available(self):
        return True