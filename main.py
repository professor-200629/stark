"""
╔═══════════════════════════════════════════════════════════════╗
║                    STARK AI ASSISTANT                         ║
║           Self-Thinking Brain - NO API Keys Needed            ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import threading
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from voice_engine import VoiceEngine
from listener import VoiceListener, KeyboardListener
from own_brain import OwnBrain
from code_brain import CodeBrain
from screen_monitor import ScreenMonitor
from camera_vision import CameraVision
from code_editor import CodeEditor
from file_explorer import FileExplorer
from browser_controller import BrowserController
from app_controller import AppController
from communication import CommunicationManager
from meeting_assistant import MeetingAssistant
from memory_manager import MemoryManager


class STARK:
    def __init__(self):
        print("\n" + "=" * 60)
        print("    STARK AI ASSISTANT - Initializing...")
        print("=" * 60 + "\n")

        print("[1/12] Loading Brain...")
        self.brain = OwnBrain()
        self.code_brain = CodeBrain()

        print("[2/12] Loading Voice Engine...")
        self.voice = VoiceEngine(config.VOICE_RATE, config.VOICE_VOLUME, config.VOICE_INDEX)

        print("[3/12] Loading Voice Listener...")
        self.listener = VoiceListener(voice_engine=self.voice)
        if not self.listener.is_available():
            print("      Voice not available, using keyboard.")
            self.listener = KeyboardListener(voice_engine=self.voice)

        print("[4/12] Loading Screen Monitor...")
        self.screen = ScreenMonitor()

        print("[5/12] Loading Camera Vision...")
        self.camera = CameraVision()

        print("[6/12] Loading Code Editor...")
        self.code_editor = CodeEditor(brain=self.brain)

        print("[7/12] Loading File Explorer...")
        self.file_explorer = FileExplorer()

        print("[8/12] Loading Browser Controller...")
        self.browser = BrowserController()

        print("[9/12] Loading App Controller...")
        self.app_ctrl = AppController()

        print("[10/12] Loading Communication...")
        self.comms = CommunicationManager()

        print("[11/12] Loading Meeting Assistant...")
        self.meeting = MeetingAssistant(brain=self.brain)

        print("[12/12] Loading Memory Manager...")
        self.memory = MemoryManager()

        self.is_running = False
        self.meeting_mode = False
        self.coding_mode = False
        self.proactive_monitoring = True
        
        self.work_start = None
        self.last_rest = time.time()
        self.last_water = time.time()
        self.last_screen_text = ""
        self.last_emotion = "neutral"

        print("\n" + "=" * 60)
        print("    STARK READY! Say 'STARK' or just speak")
        print("    Say 'shutdown' or 'exit' to quit")
        print("=" * 60 + "\n")

    def start(self):
        self.is_running = True
        self._greet()
        self.screen.start_monitoring()
        self.camera.start_camera(show_window=False)
        self.listener.start_listening()
        self.memory.start_work_session()
        self.work_start = time.time()
        
        # Callbacks for proactive monitoring
        self.camera.on_emotion_change = self._handle_emotion_change
        self.camera.on_person_detected = self._handle_person_detected
        self.screen.on_content_change = self._handle_screen_change
        
        threading.Thread(target=self._health_check, daemon=True).start()
        threading.Thread(target=self._proactive_loop, daemon=True).start()
        
        self._main_loop()

    def _greet(self):
        hour = datetime.now().hour
        if hour < 12: greeting = "Good morning"
        elif hour < 17: greeting = "Good afternoon"
        elif hour < 21: greeting = "Good evening"
        else: greeting = "Good night"
        self._speak(f"{greeting} Sir! I am STARK, your personal AI assistant. How can I make your life better today?")

    def _health_check(self):
        while self.is_running:
            time.sleep(60)
            if not self.is_running: break
            
            elapsed = time.time() - self.work_start
            
            # Rest reminder
            if time.time() - self.last_rest > config.WORK_REMINDER_INTERVAL:
                h, m = int(elapsed // 3600), int((elapsed % 3600) // 60)
                self._speak(f"Sir, you've been working for {h} hours and {m} minutes. You should take a short break to rest your eyes.")
                self.last_rest = time.time()
                
            # Water reminder
            elif time.time() - self.last_water > config.WATER_REMINDER_INTERVAL:
                self._speak("Sir, please remember to stay hydrated. Drink some water.")
                self.last_water = time.time()

    def _proactive_loop(self):
        """Loop for proactive monitoring of screen and camera"""
        while self.is_running:
            if self.proactive_monitoring:
                # Check for code on screen if in coding mode
                if self.coding_mode:
                    text = self.screen.read_screen_now()
                    if text and ("def " in text or "class " in text or "import " in text):
                        analysis = self.code_brain.full_analysis(text)
                        if "❌" in analysis: # Error found
                            self._speak("Sir, I've noticed some potential errors in your code. Would you like me to show the analysis?")
                            # We could show it automatically if meeting mode is on
                            if self.meeting_mode:
                                self.meeting.show_answer_on_screen(analysis)
            
            time.sleep(30) # Check every 30 seconds

    def _handle_emotion_change(self, emotion: str):
        if emotion != self.last_emotion:
            if emotion == "sad" or emotion == "angry" or emotion == "stressed":
                self._speak(f"Sir, you seem a bit {emotion}. Is everything alright? I'm here to help.")
            elif emotion == "happy":
                self._speak("It's good to see you happy, Sir!")
            self.last_emotion = emotion

    def _handle_person_detected(self, count: int):
        # Could alert if someone unauthorized is seen, but for now just log
        pass

    def _handle_screen_change(self, text: str):
        self.last_screen_text = text
        # If in meeting mode and someone asks a question, we could proactively help
        if self.meeting_mode:
            # Logic to detect questions and show answers
            pass

    def _speak(self, text):
        # Filter text to ensure "Sir" is present and it sounds human
        if not text.lower().startswith(("sir", "yes", "no", "of course", "sure", "i ")):
            text = f"Sir, {text}"
        
        print(f"[STARK]: {text}")
        self.voice.speak(text, wait=True)
        self.listener.notify_stark_done_speaking()

    def _main_loop(self):
        while self.is_running:
            try:
                command = self.listener.get_command(timeout=1)
                if command:
                    print(f"\n[You]: {command}")
                    self._process(command)
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                print(f"[Error] {e}")
                time.sleep(0.5)

    def _process(self, command: str):
        cmd = command.lower().strip()
        if cmd.startswith("stark "): cmd = cmd[6:].strip()
        
        # 1. SHUTDOWN & SYSTEM
        if any(w in cmd for w in ["shutdown", "exit", "quit", "goodbye", "bye"]):
            self._speak("Goodbye Sir! STARK shutting down. Have a wonderful time.")
            self.shutdown()
            return

        # 2. PERSONALITY / GREETINGS
        if any(w in cmd for w in ["how are you", "how do you feel", "what's up"]):
            self._speak(random.choice(["I am functioning perfectly, Sir! Ready to assist you.", "All systems are green, Sir! How can I help?", "I'm excellent Sir! Always a pleasure to be of service."]))
            return
        
        if any(w in cmd for w in ["hello", "hi", "hey", "stark"]):
            self._speak(random.choice(["Yes Sir!", "At your service, Sir!", "Hello Sir! What can I do for you?"]))
            return

        # 3. COMMUNICATION (WHATSAPP, TELEGRAM, CALLS)
        if "whatsapp" in cmd or "message" in cmd or "call" in cmd:
            # Handle Mummy messages/calls first
            if "mummy" in cmd or "mom" in cmd or "mother" in cmd:
                msg = self._extract_message(cmd)
                if "call" in cmd:
                    self._speak("Calling Mummy on WhatsApp, Sir.")
                    self.comms.make_whatsapp_call_to_mummy()
                else:
                    self._speak(f"Sending message to Mummy: '{msg}'")
                    self.comms.send_whatsapp_message_to_mummy(msg)
                return
            
            # General message/call logic for other contacts
            contact = self._extract_contact(cmd)
            if contact:
                msg = self._extract_message(cmd)
                if "call" in cmd:
                    self._speak(f"Calling {contact}, Sir.")
                    self.comms.make_whatsapp_call(contact)
                else:
                    self._speak(f"Sending message to {contact}: '{msg}'")
                    self.comms.send_whatsapp_message(contact, msg)
                return
            else:
                self._speak("Sir, who should I send the message to?")
                return

        # 4. YOUTUBE / SPOTIFY / MEDIA / WEBSITES
        # Handle combined "open youtube play X" command
        if "youtube" in cmd and "play" in cmd:
            query = cmd.replace("open", "").replace("youtube", "").replace("play", "").strip()
            if "in telugu" in cmd:
                query = query.replace("in telugu", "").strip() + " in telugu"
            if query:
                self._speak(f"Opening YouTube and playing {query}, Sir.")
                self.browser.youtube_search(query)
            else:
                self._speak("Opening YouTube, Sir.")
                self.browser.open_youtube()
            return
        
        # Handle "open spotify play X" command
        if "spotify" in cmd and "play" in cmd:
            song = cmd.replace("open", "").replace("spotify", "").replace("play", "").strip()
            if song:
                self._speak(f"Opening Spotify and playing {song}, Sir.")
                self.browser.search_spotify(song)
            else:
                self._speak("Opening Spotify, Sir.")
                self.browser.open_spotify()
            return
        
        # Handle simple "open youtube" without play
        if cmd.strip() == "open youtube" or cmd == "youtube":
            self._speak("Opening YouTube, Sir.")
            self.browser.open_youtube()
            return
        
        # Handle simple "open spotify" without play
        if cmd.strip() == "open spotify" or cmd == "spotify":
            self._speak("Opening Spotify, Sir.")
            self.browser.open_spotify()
            return
        
        # Handle "play X on spotify" format
        if "on spotify" in cmd and "play" in cmd:
            song = cmd.replace("play", "").replace("on spotify", "").strip()
            self._speak(f"Playing {song} on Spotify, Sir.")
            self.browser.search_spotify(song)
            return
        
        # Handle "play X on youtube" or general "play X" for videos
        if "play" in cmd:
            if "on youtube" in cmd or "video" in cmd or "trailer" in cmd or "movie" in cmd:
                query = cmd.replace("play", "").replace("on youtube", "").strip()
                self._speak(f"Searching and playing {query} on YouTube, Sir.")
                self.browser.youtube_search(query)
                return
            else:
                # Default to YouTube for play commands with songs/videos
                query = cmd.replace("play", "").strip()
                self._speak(f"Playing {query} on YouTube, Sir.")
                self.browser.youtube_search(query)
                return
        
        # Skip ad command - detect "skip" alone or "skip ad"
        if cmd.strip() in ["skip", "skip ad", "skip advertisement"]:
            self._speak("Skipping the advertisement for you, Sir.")
            self.browser.youtube_skip_ad()
            return
        
        # Media control commands
        if any(w in cmd for w in ["pause", "stop video"]):
            self._speak("Pausing playback, Sir.")
            self.browser.youtube_pause()
            return
        
        if any(w in cmd for w in ["resume", "continue", "start video"]):
            self._speak("Resuming playback, Sir.")
            self.browser.youtube_resume()
            return
        
        if "next" in cmd:
            self._speak("Playing the next video, Sir.")
            self.browser.youtube_next()
            return
        
        if "previous" in cmd or "back" in cmd:
            self._speak("Playing the previous video, Sir.")
            self.browser.youtube_previous()
            return

        # CLOSE / QUIT COMMANDS for apps and websites
        if any(w in cmd for w in ["close", "quit", "exit", "stop"]):
            if "youtube" in cmd or "video" in cmd:
                self._speak("Closing YouTube, Sir.")
                self.browser.close_tab()
                return
            if "spotify" in cmd or "music" in cmd:
                self._speak("Closing Spotify, Sir.")
                self.browser.close_tab()
                return
            if "browser" in cmd or "chrome" in cmd or "edge" in cmd:
                self._speak("Closing the browser, Sir.")
                self.browser.close_browser()
                return
            if "tab" in cmd:
                self._speak("Closing the current tab, Sir.")
                self.browser.close_tab()
                return

        # SYSTEM CONTROLS - Volume, Brightness, etc.
        if any(w in cmd for w in ["volume up", "increase volume", "louder"]):
            self._speak("Increasing volume, Sir.")
            self.browser.volume_up()
            return
        
        if any(w in cmd for w in ["volume down", "decrease volume", "quieter", "lower volume"]):
            self._speak("Decreasing volume, Sir.")
            self.browser.volume_down()
            return
        
        if any(w in cmd for w in ["mute", "unmute"]):
            self._speak("Toggling mute, Sir.")
            self.browser.volume_mute()
            return
        
        if "brightness" in cmd:
            if any(w in cmd for w in ["up", "increase", "higher", "more"]):
                self._speak("Increasing brightness, Sir.")
                # Use keyboard shortcut for brightness (if supported)
                try:
                    import pyautogui
                    pyautogui.keyDown('fn')
                    pyautogui.keyDown('f6')
                    pyautogui.keyUp('f6')
                    pyautogui.keyUp('fn')
                except:
                    pass
                return
            elif any(w in cmd for w in ["down", "decrease", "lower", "less"]):
                self._speak("Decreasing brightness, Sir.")
                try:
                    import pyautogui
                    pyautogui.keyDown('fn')
                    pyautogui.keyDown('f5')
                    pyautogui.keyUp('f5')
                    pyautogui.keyUp('fn')
                except:
                    pass
                return
        
        # Screenshot command
        if "screenshot" in cmd or "capture screen" in cmd or "take a picture" in cmd:
            self._speak("Taking a screenshot, Sir.")
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save("stark_screenshot.png")
                self._speak("Sir, screenshot saved as stark_screenshot.png.")
            except Exception as e:
                self._speak(f"Sir, I couldn't take a screenshot: {e}")
            return

        # Streaming services
        if any(w in cmd for w in ["netflix", "prime", "hotstar", "jio hotstar", "amazon prime"]):
            if "netflix" in cmd: 
                self._speak("Opening Netflix for you, Sir.")
                self.browser.open_netflix()
            elif "prime" in cmd: 
                self._speak("Opening Prime Video for you, Sir.")
                self.browser.open_prime_video()
            elif "hotstar" in cmd or "jio" in cmd: 
                self._speak("Opening JioHotstar for you, Sir.")
                self.browser.open_hotstar()
            return

        # 5. TRAVEL & LOCATION
        if "travel" in cmd or "going to" in cmd or "visit" in cmd:
            self._speak("Analyzing your travel destination, Sir. One moment.")
            response = self.brain.think(f"I am traveling to {cmd}. Suggest best hotels, restaurants, local food, and tourist attractions.")
            self._speak(response)
            return

        # 6. ROLE-BASED INTELLIGENCE
        if "act as" in cmd or "be my" in cmd:
            role = cmd.split("as")[-1].strip() if "as" in cmd else cmd.split("my")[-1].strip()
            self._speak(f"I am now your {role}, Sir. How can I assist you in this capacity?")
            # We could update the system prompt dynamically if using Gemini
            return

        # 7. SHOPPING & DESIGN
        if any(w in cmd for w in ["dress", "hairstyle", "wear", "shopping", "order"]):
            self._speak("Analyzing your request, Sir. I'll provide the best suggestions for you.")
            response = self.brain.think(cmd)
            self._speak(response)
            return

        # 8. SECURITY & CAMERA - Only for visual queries, not factual "who is" questions
        if "what do you see" in cmd or "look at" in cmd or "show me" in cmd or "identify" in cmd:
            self._speak("Let me check, Sir.")
            analysis = self.camera.analysis_result
            if analysis:
                self._speak(f"Sir, I see {analysis}")
            else:
                self._speak("Sir, I can see the environment but I'm still analyzing the details.")
            return
        
        # Facial recognition only - "who is [in the room/camera]" not "who is [famous person]"
        if "who is" in cmd and any(w in cmd for w in ["there", "here", "in the", "at the door", "behind me", "in camera"]):
            self._speak("Let me check who's there, Sir.")
            analysis = self.camera.analysis_result
            if analysis:
                self._speak(f"Sir, I see {analysis}")
            else:
                self._speak("Sir, I can see the environment but I'm still analyzing the details.")
            return

        # 9. CODING & FILE EXPLORER
        if "code" in cmd or "error" in cmd or "check" in cmd or "fix" in cmd:
            if "check" in cmd or "error" in cmd or "fix" in cmd:
                self._speak("Analyzing your code for errors, Sir.")
                text = self.screen.read_screen_now()
                if text:
                    analysis = self.code_brain.full_analysis(text)
                    self.meeting.show_answer_on_screen(analysis)
                    self._speak("Sir, I've analyzed the code. Check the meeting window for details.")
                else:
                    self._speak("Sir, I couldn't read any code from the screen.")
                return

            if "watch" in cmd or "monitor" in cmd:
                self.coding_mode = True
                self._speak("I'm now watching your code, Sir. I'll let you know if I see any mistakes.")
                return
            
            if "generate" in cmd or "create code" in cmd or "write code" in cmd:
                desc = cmd.split("generate")[-1].replace("code for", "").replace("code to", "").strip()
                if not desc:
                    desc = cmd.replace("create code", "").replace("write code", "").strip()
                self._speak(f"Generating code for {desc}, Sir.")
                code = self.code_brain.generate_code(desc)
                self.meeting.show_answer_on_screen(code)
                self._speak("Sir, I've generated the code. You can see it in the meeting window.")
                return

        # WEBSITE OPENING - Handle before file explorer
        website_keywords = {
            "amazon": ("amazon.com", "Amazon"),
            "flipkart": ("flipkart.com", "Flipkart"),
            "google": ("google.com", "Google"),
            "gmail": ("gmail.com", "Gmail"),
            "facebook": ("facebook.com", "Facebook"),
            "twitter": ("twitter.com", "Twitter"),
            "instagram": ("instagram.com", "Instagram"),
            "linkedin": ("linkedin.com", "LinkedIn"),
            "reddit": ("reddit.com", "Reddit"),
            "github": ("github.com", "GitHub"),
            "stackoverflow": ("stackoverflow.com", "Stack Overflow"),
            "wikipedia": ("wikipedia.org", "Wikipedia"),
        }
        
        for keyword, (url, name) in website_keywords.items():
            if keyword in cmd and "open" in cmd:
                self._speak(f"Opening {name} for you, Sir.")
                self.browser.open_website(url)
                return

        # FILE & FOLDER OPERATIONS
        if "file" in cmd or "folder" in cmd or "navigate" in cmd or "go to" in cmd:
            # Logic for file explorer
            if "navigate" in cmd or "go to" in cmd:
                path = cmd.split("to")[-1].strip() if "to" in cmd else cmd.split("navigate")[-1].strip()
                self._speak(self.file_explorer.navigate_to(path))
                return
            
            if "list" in cmd or "show files" in cmd or "what's here" in cmd:
                self._speak(self.file_explorer.list_contents())
                return
            
            if "search" in cmd or "find file" in cmd or "find folder" in cmd:
                filename = cmd.replace("search for", "").replace("find file", "").replace("find folder", "").replace("find", "").strip()
                self._speak(self.file_explorer.search_file(filename))
                return
            
            if "create folder" in cmd or "make folder" in cmd or "new folder" in cmd:
                folder_name = cmd.replace("create folder", "").replace("make folder", "").replace("new folder", "").strip()
                self._speak(self.file_explorer.create_folder(folder_name))
                return
            
            if "delete file" in cmd or "remove file" in cmd:
                filename = cmd.replace("delete file", "").replace("remove file", "").strip()
                self._speak(self.file_explorer.delete_file(filename))
                return
            
            if "delete folder" in cmd or "remove folder" in cmd:
                foldername = cmd.replace("delete folder", "").replace("remove folder", "").strip()
                self._speak(self.file_explorer.delete_folder(foldername))
                return

        # File operations - "open file X" or "open X" - but not websites
        if "open" in cmd:
            # Check if it's opening a file/folder vs opening an app/site
            exclude_words = ["youtube", "spotify", "netflix", "prime", "hotstar", "meeting mode", "camera", 
                           "file explorer", "amazon", "flipkart", "google", "gmail", "facebook", "twitter",
                           "instagram", "linkedin", "reddit", "github", "stackoverflow", "wikipedia"]
            if not any(word in cmd for word in exclude_words):
                filename = cmd.replace("open file", "").replace("open folder", "").replace("open", "").strip()
                if filename:
                    # Try to find and open the file
                    search_result = self.file_explorer.search_file(filename)
                    if "found" in search_result.lower():
                        # Extract path from search result
                        lines = search_result.split("\n")
                        for line in lines[1:]:  # Skip first line (header)
                            if line.strip() and not line.startswith(" "):
                                path = line.strip()
                                self._speak(self.code_editor.open_file(path))
                                return
                    # Try direct open if not found in search
                    self._speak(self.code_editor.open_file(filename))
                    return

        if "edit" in cmd or "add code" in cmd or "remove code" in cmd or "delete code" in cmd:
            if self.code_editor.current_file:
                if "add" in cmd:
                    new_code = cmd.split("add")[-1].strip()
                    self._speak(self.code_editor.append_to_file(self.code_editor.current_file, new_code))
                elif "remove" in cmd or "delete" in cmd:
                    target_text = cmd.split("remove")[-1].strip() if "remove" in cmd else cmd.split("delete")[-1].strip()
                    self._speak(self.code_editor.edit_file(self.code_editor.current_file, target_text, ""))
                elif "replace" in cmd:
                    # Format: replace [old] with [new]
                    if "with" in cmd:
                        parts = cmd.split("replace")[1].split("with")
                        if len(parts) >= 2:
                            old_text = parts[0].strip()
                            new_text = parts[1].strip()
                            self._speak(self.code_editor.edit_file(self.code_editor.current_file, old_text, new_text))
                        else:
                            self._speak("Sir, please say: replace [old text] with [new text]")
                    else:
                        self._speak("Sir, please specify what to replace with. Say: replace [old] with [new]")
                return
            else:
                self._speak("Sir, please open a file first before editing.")
                return

        # 6. MEETING MODE
        if "meeting" in cmd:
            if "start" in cmd or "on" in cmd or "activate" in cmd:
                self.meeting_mode = True
                self._speak(self.meeting.start_meeting_mode())
                return
            elif "stop" in cmd or "off" in cmd or "deactivate" in cmd:
                self.meeting_mode = False
                self._speak(self.meeting.stop_meeting_mode())
                return
        
        if "answer" in cmd and self.meeting_mode:
            question = cmd.replace("answer", "").strip()
            self._speak("Analyzing the question, Sir. One moment.")
            answer = self.brain.think(f"Answer this meeting question concisely: {question}")
            self.meeting.show_answer_on_screen(f"Q: {question}\n\nA: {answer}")
            self._speak("Sir, I've displayed the answer on screen for you.")
            return

        # 7. SCREEN READING & SUMMARIZE
        if "read" in cmd and ("screen" in cmd or "text" in cmd or "paragraph" in cmd):
            self._speak("Reading the text for you, Sir.")
            text = self.screen.read_screen_now()
            if text:
                self.last_screen_text = text
                self._speak(f"Sir, here's what it says: {text[:500]}")
            else:
                self._speak("Sir, I couldn't find any clear text to read.")
            return
        
        # Summarize command
        if "summarize" in cmd or "summarise" in cmd:
            if self.last_screen_text:
                self._speak("Summarizing the text for you, Sir.")
                summary = self.brain.think(f"Summarize this text concisely: {self.last_screen_text[:2000]}")
                self.meeting.show_answer_on_screen(f"Summary:\n\n{summary}")
                self._speak("Sir, I've displayed the summary on screen.")
            else:
                # Try to read screen first
                text = self.screen.read_screen_now()
                if text:
                    self.last_screen_text = text
                    self._speak("Summarizing the text for you, Sir.")
                    summary = self.brain.think(f"Summarize this text concisely: {text[:2000]}")
                    self.meeting.show_answer_on_screen(f"Summary:\n\n{summary}")
                    self._speak("Sir, I've displayed the summary on screen.")
                else:
                    self._speak("Sir, I don't have any text to summarize. Please read the screen first.")
            return

        # 8. JOKES
        if "joke" in cmd:
            self._speak(random.choice([
                "Sir, why do programmers prefer dark mode? Because light attracts bugs!",
                "Sir, there are 10 types of people: those who understand binary and those who don't.",
                "Sir, a SQL query walks into a bar, sees two tables, asks: Can I JOIN you?",
            ]))
            return

        # 10. TIMER & REMINDERS
        if "timer" in cmd or "alarm" in cmd or "remind me" in cmd:
            self._handle_timer(cmd)
            return
        
        # GENERAL BRAIN - For all other questions and knowledge queries
        # Prepare context for better responses
        query_context = ""
        if "how to" in cmd or "what is" in cmd or "who is" in cmd or "why" in cmd or "when" in cmd:
            query_context = "This is a factual question. Provide a clear, informative answer."
        
        response = self.brain.think(cmd, context=self.last_screen_text or query_context)
        self._speak(response)
        
        if response:
            self.memory.add_conversation(cmd, str(response)[:200])

    def shutdown(self):
        print("\n[STARK] Shutting down...")
        self.is_running = False
        for name, cleanup in [
            ("Camera", lambda: self.camera.stop_camera()),
            ("Screen", lambda: self.screen.stop_monitoring()),
            ("Listener", lambda: self.listener.stop_listening()),
            ("Meeting", lambda: self.meeting.close()),
            ("Memory", lambda: (self.memory.end_work_session(), self.memory.save())),
            ("Voice", lambda: self.voice.shutdown()),
        ]:
            try:
                cleanup()
            except Exception as e:
                print(f"[STARK] Error stopping {name}: {e}")
        print("[STARK] Goodbye Sir!")
        sys.exit()

    def _extract_contact(self, cmd: str) -> str:
        """Extract contact name from command."""
        # Known contact keywords to look for
        contacts = ["mummy", "mom", "mother", "dad", "father", "friend", "brother", "sister", 
                   "uncle", "aunty", "boss", "colleague", "teacher", "doctor"]
        
        # Check for "message/call [contact]" pattern
        for keyword in ["message", "call", "whatsapp", "text"]:
            if keyword in cmd:
                parts = cmd.split(keyword, 1)
                if len(parts) > 1:
                    potential = parts[1].strip()
                    # Check if it starts with a known contact
                    for contact in contacts:
                        if potential.startswith(contact) or f" {contact} " in potential:
                            return contact
                    # Return first word if it's not a message content word
                    first_word = potential.split()[0] if potential.split() else ""
                    if first_word and first_word not in ["saying", "that", "hello", "hi", "to", "on"]:
                        return first_word
        return ""

    def _extract_message(self, cmd: str) -> str:
        """Extract message content from command."""
        # Look for content after "saying", "that", or the contact name
        separators = ["saying", "that", "to say", "message"]
        for sep in separators:
            if sep in cmd:
                parts = cmd.split(sep, 1)
                if len(parts) > 1:
                    msg = parts[1].strip()
                    # Remove trailing phrases
                    for end in [" on whatsapp", " via whatsapp", " please", " now"]:
                        if msg.endswith(end):
                            msg = msg[:-len(end)]
                    return msg
        
        # If no separator found, return a default greeting
        return "Hello!"

    def _handle_timer(self, cmd: str):
        """Handle timer and alarm commands."""
        import re
        
        # Extract numbers from command
        numbers = re.findall(r'(\d+)', cmd)
        if not numbers:
            self._speak("Sir, please specify a time. For example: 'set timer for 5 minutes' or 'remind me in 10 minutes'.")
            return
        
        value = int(numbers[0])
        seconds = 0
        
        # Determine unit
        if "hour" in cmd:
            seconds = value * 3600
            unit = f"{value} hour{'s' if value > 1 else ''}"
        elif "minute" in cmd:
            seconds = value * 60
            unit = f"{value} minute{'s' if value > 1 else ''}"
        elif "second" in cmd:
            seconds = value
            unit = f"{value} second{'s' if value > 1 else ''}"
        else:
            # Default to minutes if no unit specified
            seconds = value * 60
            unit = f"{value} minute{'s' if value > 1 else ''}"
        
        self._speak(f"Sir, timer set for {unit}.")
        
        # Start timer in background thread
        def timer_callback():
            time.sleep(seconds)
            self._speak(f"Sir, your timer for {unit} is up!")
            # Try to show notification if on Windows
            try:
                if os.name == 'nt':
                    import ctypes
                    ctypes.windll.user32.MessageBoxW(0, f"Timer: {unit} has passed!", "STARK Timer", 0x40)
            except Exception:
                pass
        
        import threading
        threading.Thread(target=timer_callback, daemon=True).start()


if __name__ == "__main__":
    try:
        stark = STARK()
        stark.start()
    except KeyboardInterrupt:
        print("\n[STARK] Interrupted.")
    except Exception as e:
        print(f"\n[STARK] Error: {e}")
        import traceback
        traceback.print_exc()
