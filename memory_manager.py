"""
STARK Memory Manager - Long-term Memory and Learning
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class MemoryManager:
    """Manages STARK's long-term memory"""

    def __init__(self):
        self.memory_file = config.MEMORY_FILE
        self.memory = {
            "user_profile": {
                "name": config.USER_NAME,
                "preferences": {},
                "habits": {},
                "goals": []
            },
            "conversations": [],
            "reminders": [],
            "notes": [],
            "learned_facts": {},
            "work_sessions": [],
            "mood_history": [],
            "important_dates": [],
            "contacts": config.CONTACTS.copy(),
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

        self._load_memory()
        print("[Memory] Loaded and ready.")

    def _load_memory(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    for key in saved:
                        if key in self.memory:
                            if isinstance(self.memory[key], dict):
                                self.memory[key].update(saved[key])
                            else:
                                self.memory[key] = saved[key]
        except Exception as e:
            print(f"[Memory] Error loading: {e}")

    def save(self):
        try:
            self.memory["last_updated"] = datetime.now().isoformat()
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Memory] Error saving: {e}")

    # ========== USER PROFILE ==========

    def set_preference(self, key: str, value: Any):
        self.memory["user_profile"]["preferences"][key] = value
        self.save()

    def get_preference(self, key: str, default=None) -> Any:
        return self.memory["user_profile"]["preferences"].get(key, default)

    def set_habit(self, habit: str, details: str):
        self.memory["user_profile"]["habits"][habit] = {
            "details": details,
            "recorded": datetime.now().isoformat()
        }
        self.save()

    def get_habit(self, habit: str) -> Optional[str]:
        if habit in self.memory["user_profile"]["habits"]:
            return self.memory["user_profile"]["habits"][habit]["details"]
        return None

    def add_goal(self, goal: str):
        self.memory["user_profile"]["goals"].append({
            "goal": goal,
            "added": datetime.now().isoformat(),
            "completed": False
        })
        self.save()

    def get_active_goals(self) -> List[Dict]:
        return [g for g in self.memory["user_profile"]["goals"] if not g.get("completed")]

    # ========== CONVERSATIONS ==========

    def add_conversation(self, user_input: str, response: str):
        self.memory["conversations"].append({
            "user": user_input[:500],
            "stark": response[:500],
            "time": datetime.now().isoformat()
        })

        if len(self.memory["conversations"]) > 100:
            self.memory["conversations"] = self.memory["conversations"][-100:]

        self.save()

    def get_recent_conversations(self, count: int = 10) -> List[Dict]:
        return self.memory["conversations"][-count:]

    # ========== REMINDERS ==========

    def add_reminder(self, text: str, time_str: str = None, recurring: str = None):
        reminder = {
            "text": text,
            "created": datetime.now().isoformat(),
            "time": time_str,
            "recurring": recurring,
            "completed": False,
            "notified": False
        }
        self.memory["reminders"].append(reminder)
        self.save()
        return reminder

    def get_reminders(self, include_completed: bool = False) -> List[Dict]:
        if include_completed:
            return self.memory["reminders"]
        return [r for r in self.memory["reminders"] if not r.get("completed")]

    def complete_reminder(self, index: int):
        if 0 <= index < len(self.memory["reminders"]):
            self.memory["reminders"][index]["completed"] = True
            self.memory["reminders"][index]["completed_at"] = datetime.now().isoformat()
            self.save()

    def delete_reminder(self, index: int):
        if 0 <= index < len(self.memory["reminders"]):
            self.memory["reminders"].pop(index)
            self.save()

    # ========== NOTES ==========

    def add_note(self, text: str, category: str = "general"):
        self.memory["notes"].append({
            "text": text,
            "category": category,
            "created": datetime.now().isoformat()
        })
        self.save()

    def get_notes(self, category: str = None) -> List[Dict]:
        if category:
            return [n for n in self.memory["notes"] if n.get("category") == category]
        return self.memory["notes"]

    # ========== WORK SESSIONS ==========

    def start_work_session(self):
        session = {
            "start": datetime.now().isoformat(),
            "end": None,
            "duration_minutes": None
        }
        self.memory["work_sessions"].append(session)
        self.save()

    def end_work_session(self):
        if self.memory["work_sessions"]:
            last = self.memory["work_sessions"][-1]
            if last["end"] is None:
                last["end"] = datetime.now().isoformat()
                start = datetime.fromisoformat(last["start"])
                end = datetime.fromisoformat(last["end"])
                last["duration_minutes"] = int((end - start).total_seconds() / 60)
                self.save()

    # ========== CONTACTS ==========

    def add_contact(self, name: str, number: str, email: str = None):
        self.memory["contacts"][name.lower()] = number
        self.save()

    def get_contact(self, name: str) -> Optional[str]:
        return self.memory["contacts"].get(name.lower())

    # ========== SUMMARY ==========

    def get_summary(self) -> str:
        return f"""Sir, here's what I remember:
• Conversations: {len(self.memory['conversations'])}
• Reminders: {len([r for r in self.memory['reminders'] if not r.get('completed')])} active
• Notes: {len(self.memory['notes'])}
• Goals: {len(self.get_active_goals())} active
• Work sessions: {len(self.memory['work_sessions'])}
• Contacts: {len(self.memory['contacts'])}

Last updated: {self.memory.get('last_updated', 'Never')}"""