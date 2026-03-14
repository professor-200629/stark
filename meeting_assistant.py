"""
STARK Meeting Assistant - Live Meeting Help
Shows answers on screen (no voice) during meetings
"""

import threading
import time
from datetime import datetime

import config


class MeetingAssistant:
    """Assistant for online meetings - Shows answers on screen silently"""

    def __init__(self, brain=None):
        self.brain = brain
        self.is_active = False
        self.meeting_context = []
        self.current_answer = ""
        self.on_question_detected = None

        self._tk_root = None
        self._tk_label = None
        self._tk_thread = None
        self._tk_ready = threading.Event()

        print("[MeetingAssistant] Ready for meetings.")

    def _ensure_tk(self):
        if self._tk_thread is not None:
            self._tk_ready.wait(timeout=5)
            return

        self._tk_thread = threading.Thread(target=self._tk_loop, daemon=True, name="MeetingTk")
        self._tk_thread.start()
        self._tk_ready.wait(timeout=5)

    def _tk_loop(self):
        try:
            import tkinter as tk
            from tkinter import font as tkfont

            root = tk.Tk()
            root.title("STARK - Meeting Assistant")
            root.geometry("500x400")
            root.configure(bg='#1a1a2e')
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.95)

            screen_w = root.winfo_screenwidth()
            root.geometry(f"500x400+{screen_w - 520}+50")

            title_f = tkfont.Font(family='Helvetica', size=14, weight='bold')
            tk.Label(root, text="STARK - Meeting Helper", font=title_f,
                     bg='#1a1a2e', fg='#00ff88').pack(pady=10)

            answer_f = tkfont.Font(family='Helvetica', size=12)
            label = tk.Label(root, text="Waiting for questions...", font=answer_f,
                             bg='#1a1a2e', fg='#ffffff', wraplength=450, justify='left')
            label.pack(pady=20, padx=20, fill='both', expand=True)

            inst_f = tkfont.Font(family='Helvetica', size=9)
            tk.Label(root, text="Say 'answer [question]' to get help\nThis window is visible only to you",
                     font=inst_f, bg='#1a1a2e', fg='#888888').pack(pady=5)

            root.withdraw()

            self._tk_root = root
            self._tk_label = label
            self._tk_ready.set()

            root.mainloop()
        except Exception as e:
            print(f"[MeetingAssistant] Tk init error: {e}")
            self._tk_ready.set()

    def _tk_run(self, fn):
        if self._tk_root is None:
            return
        try:
            self._tk_root.after(0, fn)
        except Exception:
            pass

    def start_meeting_mode(self) -> str:
        self.is_active = True
        self.meeting_context = []

        self._ensure_tk()
        self._tk_run(lambda: (self._tk_root.deiconify(), self._tk_root.lift()))

        return "Sir, meeting mode activated. I'll show answers on screen. Just say 'answer' followed by your question."

    def stop_meeting_mode(self) -> str:
        self.is_active = False
        self._tk_run(lambda: self._tk_root.withdraw())
        return "Sir, meeting mode deactivated. Good luck with the rest of your meeting!"

    def show_answer_on_screen(self, question: str) -> str:
        if not self.is_active:
            self.start_meeting_mode()

        answer = self._generate_answer(question)

        self.meeting_context.append({
            "question": question,
            "answer": answer,
            "time": datetime.now().isoformat()
        })

        self._display_answer(question, answer)
        return answer

    def _generate_answer(self, question: str) -> str:
        if self.brain:
            return self.brain.answer_meeting_question(question)

        question_lower = question.lower()

        if "tell me about yourself" in question_lower or "introduce yourself" in question_lower:
            return ("I'm a dedicated professional with experience in my field. "
                    "I'm passionate about continuous learning and delivering quality work. "
                    "I believe in collaborative problem-solving and effective communication.")

        if "experience" in question_lower:
            return ("I have hands-on experience working on various projects. "
                    "I enjoy taking on challenges and learning from each opportunity.")

        if "strength" in question_lower:
            return ("My key strengths include problem-solving, attention to detail, "
                    "strong communication, and adaptability.")

        if "weakness" in question_lower:
            return ("I sometimes focus too much on details, but I've been working on "
                    "balancing perfectionism with efficiency.")

        if "why do you want" in question_lower or "why should we" in question_lower:
            return ("The role aligns with my skills and interests. I see great potential "
                    "for growth and I'm eager to bring my abilities to the team.")

        if "challenge" in question_lower or "difficult situation" in question_lower:
            return ("I approach challenges by understanding the problem thoroughly, "
                    "breaking it into parts, seeking team input, and implementing systematic solutions.")

        if "where do you see yourself" in question_lower:
            return ("I see myself growing professionally, taking on more responsibilities, "
                    "and contributing meaningfully to the organization.")

        if "salary" in question_lower or "compensation" in question_lower:
            return ("I'm open to discussing compensation based on the role and responsibilities. "
                    "I'm more focused on finding the right fit and growth opportunity.")

        if "python" in question_lower:
            return ("Python is a versatile, easy-to-read language great for automation, "
                    "data analysis, and web development with a rich ecosystem of libraries.")

        if "api" in question_lower:
            return ("API stands for Application Programming Interface. It allows different "
                    "software systems to communicate using standard request/response patterns.")

        if "database" in question_lower:
            return ("Databases store organized data. SQL databases like MySQL use tables; "
                    "NoSQL databases like MongoDB use flexible documents.")

        return (f"For the question about '{question[:40]}...': "
                "Structure your answer as Situation > Action > Result. "
                "Be specific with examples and stay confident.")

    def _display_answer(self, question: str, answer: str):
        print(f"\n{'=' * 50}")
        print(f"[MEETING ANSWER]")
        print(f"Q: {question}")
        print(f"A: {answer}")
        print(f"{'=' * 50}\n")

        display_text = f"Question:\n{question}\n\nAnswer:\n{answer}"
        self._tk_run(lambda: self._update_label(display_text))

    def _update_label(self, text):
        if self._tk_label:
            self._tk_label.config(text=text)
        if self._tk_root:
            self._tk_root.lift()

    def add_context(self, context: str):
        self.meeting_context.append({"context": context, "time": datetime.now().isoformat()})

    def get_meeting_summary(self) -> str:
        if not self.meeting_context:
            return "Sir, no meeting context recorded yet."
        return (f"Sir, meeting summary: {len(self.meeting_context)} questions addressed, "
                f"started at {self.meeting_context[0].get('time', 'N/A')}.")

    def suggest_response(self, topic: str) -> str:
        return self._generate_answer(topic)

    def hide_display(self):
        self._tk_run(lambda: self._tk_root.withdraw())

    def show_display(self):
        self._ensure_tk()
        self._tk_run(lambda: (self._tk_root.deiconify(), self._tk_root.lift()))

    def close(self):
        self.is_active = False
        if self._tk_root:
            try:
                self._tk_root.after(0, self._tk_root.destroy)
            except Exception:
                pass
        print("[MeetingAssistant] Closed.")