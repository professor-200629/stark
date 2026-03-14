"""
STARK Communication - WhatsApp, Telegram, Instagram, Snapchat, Email
"""

import time
import webbrowser
import subprocess
import urllib.parse

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from .utils import safe_type as _safe_type


class CommunicationManager:
    """Manage communications across platforms"""

    def __init__(self):
        self.contacts = config.CONTACTS.copy()
        self.message_history = []
        print("[Communication] Manager initialized.")

    def _resolve_contact(self, name: str) -> str:
        name_lower = name.lower().strip()

        for key, number in self.contacts.items():
            if key in name_lower or name_lower in key:
                return number

        if name.startswith("+") or name.replace(" ", "").isdigit():
            return name.replace(" ", "")

        return None

    # ========== WHATSAPP ==========

    def send_whatsapp_message(self, contact: str, message: str) -> str:
        number = self._resolve_contact(contact)

        if not number:
            return f"Sir, I don't have a number for '{contact}'."

        try:
            url = f"https://web.whatsapp.com/send?phone={number}&text={urllib.parse.quote(message)}"
            webbrowser.open(url)
            time.sleep(8)

            if PYAUTOGUI_AVAILABLE:
                pyautogui.press('enter')

            self._log_message("whatsapp", contact, message)
            return f"Sir, message sent to {contact} on WhatsApp."

        except Exception as e:
            return f"Sir, couldn't send WhatsApp message: {e}"

    def send_whatsapp_message_to_mummy(self, message: str) -> str:
        return self.send_whatsapp_message("mummy", message)

    def make_whatsapp_call(self, contact: str, video: bool = False) -> str:
        number = self._resolve_contact(contact)

        if not number:
            return f"Sir, I don't have a number for '{contact}'."

        try:
            # WhatsApp desktop app protocol for calling
            # Note: This requires the WhatsApp Desktop app to be installed
            call_type = "video" if video else "voice"
            
            # For web, we can only open the chat. 
            # For desktop app, we might be able to trigger more.
            url = f"https://web.whatsapp.com/send?phone={number}"
            webbrowser.open(url)
            time.sleep(5)
            
            if PYAUTOGUI_AVAILABLE:
                # Try to click the call button (approximate location)
                # This is tricky as locations vary, but we can try common shortcuts
                # if the app is focused.
                pass

            return f"Sir, I've opened the WhatsApp chat with {contact}. You can start the {call_type} call now."

        except Exception as e:
            return f"Sir, couldn't initiate WhatsApp call: {e}"

    def make_whatsapp_call_to_mummy(self, video: bool = False) -> str:
        return self.make_whatsapp_call("mummy", video)

    # ========== TELEGRAM ==========

    def send_telegram_message(self, contact: str, message: str) -> str:
        try:
            # Try to use telegram desktop protocol
            url = f"tg://msg?text={urllib.parse.quote(message)}&to={contact}"
            try:
                os.startfile(url)
            except Exception:
                webbrowser.open(f"https://web.telegram.org/k/#?q={contact}")
                time.sleep(5)
                if PYAUTOGUI_AVAILABLE:
                    _safe_type(message)
                    pyautogui.press('enter')

            self._log_message("telegram", contact, message)
            return f"Sir, message sent to {contact} on Telegram."

        except Exception as e:
            return f"Sir, couldn't send Telegram message: {e}"

    def open_telegram(self) -> str:
        try:
            subprocess.Popen("telegram", shell=True)
        except Exception:
            webbrowser.open("https://web.telegram.org")
        return "Sir, Telegram is open."

    # ========== INSTAGRAM ==========

    def open_instagram(self) -> str:
        webbrowser.open("https://www.instagram.com")
        return "Sir, Instagram is open."

    def send_instagram_dm(self, contact: str, message: str) -> str:
        try:
            # Instagram doesn't have a direct URL for sending a message to a specific user
            # We open the inbox and try to search
            webbrowser.open("https://www.instagram.com/direct/inbox/")
            time.sleep(5)
            
            if PYAUTOGUI_AVAILABLE:
                # Search for contact
                pyautogui.press('tab')
                time.sleep(0.5)
                _safe_type(contact)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                _safe_type(message)
                pyautogui.press('enter')
                
            return f"Sir, I've attempted to send an Instagram DM to {contact}."
        except Exception as e:
            return f"Sir, error with Instagram: {e}"

    # ========== SNAPCHAT ==========

    def open_snapchat(self) -> str:
        webbrowser.open("https://web.snapchat.com")
        return "Sir, Snapchat is open."

    def send_snapchat_message(self, contact: str, message: str) -> str:
        webbrowser.open(f"https://web.snapchat.com/")
        return f"Sir, Snapchat web is open. Please select {contact} to send your message."

    # ========== EMAIL ==========

    def send_email(self, to: str, subject: str, body: str) -> str:
        try:
            params = urllib.parse.urlencode({
                'to': to,
                'subject': subject,
                'body': body
            })
            webbrowser.open(f"https://mail.google.com/mail/?view=cm&{params}")
            return f"Sir, Gmail compose opened for {to}."
        except Exception as e:
            return f"Sir, couldn't open email: {e}"

    # ========== CONTACTS MANAGEMENT ==========

    def add_contact(self, name: str, number: str) -> str:
        self.contacts[name.lower()] = number
        return f"Sir, added contact: {name} - {number}"

    def get_contact(self, name: str) -> str:
        number = self._resolve_contact(name)
        if number:
            return f"Sir, {name}'s number is {number}"
        return f"Sir, no contact found for '{name}'"

    def list_contacts(self) -> str:
        if not self.contacts:
            return "Sir, no contacts saved."

        result = "Sir, here are your contacts:\n"
        for name, number in self.contacts.items():
            result += f"  • {name.title()}: {number}\n"
        return result

    def remove_contact(self, name: str) -> str:
        name_lower = name.lower()
        if name_lower in self.contacts:
            del self.contacts[name_lower]
            return f"Sir, removed contact: {name}"
        return f"Sir, no contact found for '{name}'"

    # ========== MESSAGE HISTORY ==========

    def _log_message(self, platform: str, contact: str, message: str):
        from datetime import datetime
        self.message_history.append({
            "platform": platform,
            "contact": contact,
            "message": message,
            "time": datetime.now().isoformat()
        })

        if len(self.message_history) > 50:
            self.message_history.pop(0)

    def get_message_history(self, count: int = 10) -> str:
        if not self.message_history:
            return "Sir, no messages sent yet."

        recent = self.message_history[-count:]
        result = "Sir, recent messages:\n"
        for msg in recent:
            result += f"  • [{msg['platform']}] {msg['contact']}: {msg['message'][:30]}...\n"
        return result

    # ========== QUICK ACTIONS ==========

    def quick_message_mummy(self, message_type: str = "hello") -> str:
        messages = {
            "hello": "Hello Mummy! How are you?",
            "goodmorning": "Good Morning Mummy! Have a great day!",
            "goodnight": "Good Night Mummy! Sleep well!",
            "eating": "Mummy, I'm eating now.",
            "reached": "Mummy, I've reached safely.",
            "coming": "Mummy, I'm coming home.",
            "busy": "Mummy, I'm busy right now. Will call later.",
            "ok": "Okay Mummy!",
        }

        message = messages.get(message_type.lower(), message_type)
        return self.send_whatsapp_message_to_mummy(message)