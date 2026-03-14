"""
STARK Own Brain - Self-Thinking AI
NO API KEYS NEEDED - Fully independent intelligent responses
"""

import random
import re
import json
import os
from datetime import datetime
from typing import Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False

import config
from knowledge_engine import KnowledgeEngine


class OwnBrain:
    """
    STARK's Self-Thinking Brain
    Works without any API keys using intelligent pattern matching
    and local knowledge processing
    """

    def __init__(self):
        self.knowledge = KnowledgeEngine()
        self.context = []
        self.gemini_model = None
        self.gemini_chat = None
        self.use_gemini = False
        self._init_ai()
        self._load_memory()

    def _init_ai(self):
        if GEMINI_AVAILABLE and config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=config.GEMINI_API_KEY)
                model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    system_instruction=(
                        "You are STARK, a personal AI assistant. "
                        "Call the user 'Sir' always. Be friendly, loyal, calm, proactive. "
                        "Keep responses under 80 words for voice output. "
                        "When giving code, make it complete and working."
                    )
                )
                self.gemini_chat = model.start_chat(history=[])
                self.use_gemini = True
                print("[Brain] Gemini AI connected!")
            except Exception as e:
                print(f"[Brain] Gemini error: {e}")

        if not self.use_gemini:
            print("[Brain] Running in local mode (no API needed).")

    def _load_memory(self):
        try:
            if os.path.exists(config.MEMORY_FILE):
                with open(config.MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                    if 'learned_responses' in data:
                        self.knowledge.knowledge.setdefault('learned', {})
                        self.knowledge.knowledge['learned'] = data.get('learned_responses', {})
        except Exception:
            pass

    def think(self, user_input: str, context: str = None) -> str:
        """Main thinking function"""
        user_input = user_input.strip()

        self.context.append({"role": "user", "content": user_input})
        if len(self.context) > 10:
            self.context = self.context[-10:]

        # Check knowledge engine first
        response = self._check_knowledge(user_input)
        if response:
            return response

        # Try Gemini if available
        if self.use_gemini and self.gemini_chat:
            try:
                prompt = user_input
                if context:
                    prompt = f"Context: {context}\n\nUser says: {user_input}"
                response = self.gemini_chat.send_message(prompt)
                if response and response.text:
                    return self._format_response(response.text)
            except Exception as e:
                print(f"[Brain] Gemini error: {e}")

        # Use local brain fallback
        return self._local_think(user_input, context)

    def _check_knowledge(self, user_input: str) -> Optional[str]:
        """Check all knowledge sources for quick responses"""
        greeting = self.knowledge.get_greeting(user_input)
        if greeting:
            return greeting

        about = self.knowledge.get_about(user_input)
        if about:
            return about

        code = self.knowledge.get_code_template(user_input)
        if code:
            return f"Sir, here's the code you requested:\n\n{code}"

        subject = self.knowledge.get_subject_info(user_input)
        if subject:
            return subject

        error_help = self.knowledge.get_error_help(user_input)
        if error_help:
            return f"Sir, {error_help}"

        return None

    def _format_response(self, response: str) -> str:
        """Format AI response for voice output"""
        response = response.replace("**", "").replace("```", "")
        response = response.replace("STARK:", "").strip()
        if not response.lower().startswith(("sir", "yes", "no", "i ", "here", "sure", "of course")):
            response = f"Sir, {response}"
        return response

    def _local_think(self, user_input: str, context: str = None) -> str:
        """Local thinking without external API"""
        input_lower = user_input.lower()

        # ========== TIME & DATE ==========
        if any(w in input_lower for w in ["what time", "current time", "tell me the time"]):
            return f"Sir, the current time is {datetime.now().strftime('%I:%M %p')}."

        if any(w in input_lower for w in ["what date", "today's date", "current date", "what day"]):
            return f"Sir, today is {datetime.now().strftime('%A, %B %d, %Y')}."

        # ========== HEALTH TIP ==========
        if any(w in input_lower for w in ["health tip", "health advice", "stay healthy"]):
            return self.knowledge.get_health_tip()

        # ========== MOTIVATION ==========
        if any(w in input_lower for w in ["motivat", "inspire", "encourage", "quote"]):
            return self.knowledge.get_motivation()

        # ========== THANK YOU ==========
        if any(w in input_lower for w in ["thank", "thanks", "appreciate", "thank you"]):
            return random.choice([
                "You're welcome, Sir! Always here for you.",
                "My pleasure, Sir! Anything else?",
                "Happy to help, Sir!",
                "Anytime, Sir!"
            ])

        # ========== JOKE ==========
        if any(w in input_lower for w in ["joke", "funny", "make me laugh"]):
            jokes = [
                "Sir, why do programmers prefer dark mode? Because light attracts bugs!",
                "Sir, why did the developer go broke? He used up all his cache!",
                "Sir, there are only 10 types of people: those who understand binary and those who don't.",
                "Sir, a SQL query walks into a bar and asks two tables: 'Can I JOIN you?'",
            ]
            return random.choice(jokes)

        # ========== WEATHER ==========
        if "weather" in input_lower:
            return "Sir, I need web access to check the weather. I can open a weather website if you'd like."

        # ========== CODE GENERATION ==========
        if any(w in input_lower for w in ["generate code", "write code", "create code", "code for", "write a program"]):
            return self._generate_code_locally(input_lower)

        # ========== EXPLANATIONS ==========
        if any(w in input_lower for w in ["explain", "teach me", "what is", "tell me about", "how does", "how do", "how to", "who is", "who was", "what are"]):
            return self._explain_topic(input_lower)

        # ========== CALCULATIONS ==========
        if any(op in input_lower for op in ["calculate", "compute"]) or (
            any(op in input_lower for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided"]) and
            any(c.isdigit() for c in input_lower)
        ):
            return self._try_calculate(input_lower)

        # ========== SEARCH ALL KNOWLEDGE ==========
        knowledge_result = self.knowledge.search_all_knowledge(input_lower)
        if knowledge_result:
            return knowledge_result

        # ========== GENERAL FALLBACK ==========
        return self._generate_general_response(input_lower)

    def _generate_code_locally(self, input_lower: str) -> str:
        template = self.knowledge.get_code_template(input_lower)
        if template:
            return f"Sir, here's the code:\n\n{template}"

        if "calculator" in input_lower:
            return self.knowledge.code_templates.get("calculator", "")
        if any(w in input_lower for w in ["todo", "task", "list"]):
            return self.knowledge.code_templates.get("todo list", "")
        if "scraper" in input_lower:
            return self.knowledge.code_templates.get("web scraper", "")
        if "password" in input_lower:
            return self.knowledge.code_templates.get("password generator", "")

        return ("Sir, I can generate code! Available templates: calculator, todo list, "
                "web scraper, password generator, website, login page, flask app, rest api, "
                "chat bot, quiz app, guessing game, file organizer.")

    def _explain_topic(self, input_lower: str) -> str:
        info = self.knowledge.get_subject_info(input_lower)
        if info:
            return info

        topic = input_lower
        for word in ["explain", "teach me", "what is", "tell me about", "how does", "how do", "about", "work"]:
            topic = topic.replace(word, "")
        topic = topic.strip()

        if topic:
            # Provide a more helpful response with web search suggestion
            return (f"Sir, I don't have specific information about '{topic}' in my local knowledge base. "
                    f"I can search the web for you — just say 'search {topic}' and I'll look it up on Google.")
        return "Sir, please tell me what topic you'd like me to explain."

    def _try_calculate(self, input_lower: str) -> str:
        try:
            numbers = re.findall(r'\d+(?:\.\d+)?', input_lower)
            if len(numbers) >= 2:
                a, b = float(numbers[0]), float(numbers[1])
                if any(w in input_lower for w in ["plus", "+", "add"]):
                    return f"Sir, {numbers[0]} plus {numbers[1]} equals {a + b}."
                if any(w in input_lower for w in ["minus", "-", "subtract"]):
                    return f"Sir, {numbers[0]} minus {numbers[1]} equals {a - b}."
                if any(w in input_lower for w in ["times", "*", "multiply", "multiplied"]):
                    return f"Sir, {numbers[0]} times {numbers[1]} equals {a * b}."
                if any(w in input_lower for w in ["divided", "/", "divide"]):
                    if b == 0:
                        return "Sir, cannot divide by zero!"
                    return f"Sir, {numbers[0]} divided by {numbers[1]} equals {a / b:.4f}."
        except Exception:
            pass
        return "Sir, I couldn't perform that calculation. Please phrase it differently."

    def _generate_general_response(self, input_lower: str) -> str:
        """Generate a meaningful general response"""
        question_words = ["what", "how", "why", "when", "where", "who", "which", "can", "could", "would", "should"]

        if any(w in input_lower for w in question_words) or input_lower.endswith("?"):
            # Build a concise search query by stripping leading question words
            topic = input_lower.rstrip("?").strip()
            for qw in ["what is", "what are", "how to", "how do", "how does", "who is", "who was",
                       "why is", "why does", "when is", "where is", "which is"]:
                if topic.startswith(qw + " "):
                    topic = topic[len(qw):].strip()
                    break
            return (f"Sir, I don't have enough local information to answer that confidently. "
                    f"Say 'search {topic}' and I'll look it up on Google for you right away.")
        else:
            responses = [
                "I understand, Sir. Is there anything specific you'd like me to help with?",
                "Got it, Sir. Let me know if you need assistance with anything.",
                "Understood, Sir. I'm here whenever you need me.",
                "Sir, I'm listening. What would you like to do next?",
            ]
        return random.choice(responses)

    def analyze_screen(self, screen_text: str) -> str:
        """Analyze screen content"""
        if not screen_text:
            return "Sir, I couldn't read any text from the screen."

        if self.use_gemini and self.gemini_chat:
            try:
                prompt = f"Summarize what's on this screen in 3 sentences:\n\n{screen_text[:2000]}"
                response = self.gemini_chat.send_message(prompt)
                if response and response.text:
                    return f"Sir, {response.text}"
            except Exception:
                pass

        lines = screen_text.split('\n')
        words = screen_text.split()
        return (f"Sir, I can see content on your screen with {len(lines)} lines and {len(words)} words. "
                "Would you like me to summarize it or look for something specific?")

    def analyze_code(self, code: str, language: str = "python") -> str:
        """Analyze code for errors"""
        if not code:
            return "Sir, I couldn't read any code from the screen."

        errors_found = []

        if "python" in language.lower():
            if "print " in code and "print(" not in code:
                errors_found.append("Print statement missing parentheses — use print() not print")
            open_brackets = code.count('(') + code.count('[') + code.count('{')
            close_brackets = code.count(')') + code.count(']') + code.count('}')
            if open_brackets != close_brackets:
                errors_found.append(f"Unmatched brackets: {open_brackets} open, {close_brackets} close")

        if self.use_gemini and self.gemini_chat:
            try:
                prompt = f"Analyze this {language} code for errors. Be concise:\n\n```{language}\n{code[:2000]}\n```"
                response = self.gemini_chat.send_message(prompt)
                if response and response.text:
                    return f"Sir, {response.text}"
            except Exception:
                pass

        result = "Sir, I've analyzed your code.\n"
        if errors_found:
            result += "Potential issues:\n" + "\n".join(f"• {e}" for e in errors_found)
        else:
            result += "No obvious errors detected. Would you like me to help with anything specific?"
        return result

    def answer_meeting_question(self, question: str, context: str = None) -> str:
        """Generate answer for meeting questions"""
        if self.use_gemini and self.gemini_chat:
            try:
                prompt = (
                    f"I'm in a meeting. Someone asked:\n{question}\n\n"
                    f"{'Context: ' + context if context else ''}\n"
                    "Give a clear, professional answer I can read. Be concise but complete."
                )
                response = self.gemini_chat.send_message(prompt)
                if response and response.text:
                    return response.text
            except Exception:
                pass

        question_lower = question.lower()

        if any(w in question_lower for w in ["introduce", "tell us about yourself", "who are you"]):
            return ("I'm a dedicated professional with hands-on experience in my field. "
                    "I'm passionate about continuous learning and delivering quality work. "
                    "I believe in collaborative problem-solving and effective communication.")

        if "experience" in question_lower:
            return ("I have practical experience working on various projects and challenges. "
                    "Each project has taught me valuable skills and I'm always eager to apply what I've learned.")

        if "strength" in question_lower:
            return ("My key strengths include problem-solving, attention to detail, "
                    "strong communication skills, and the ability to adapt quickly to new situations.")

        if "weakness" in question_lower:
            return ("I sometimes focus too much on details to ensure accuracy, "
                    "but I've been actively working on balancing thoroughness with efficiency.")

        if any(w in question_lower for w in ["why do you want", "why should we hire", "why this"]):
            return ("This opportunity aligns perfectly with my skills and career goals. "
                    "I see great potential for growth here and I'm eager to contribute meaningfully to the team.")

        if any(w in question_lower for w in ["challenge", "difficult situation", "problem you solved"]):
            return ("I faced a challenging deadline where the requirements changed last minute. "
                    "I broke the problem into smaller tasks, communicated clearly with the team, "
                    "and we delivered on time by prioritizing effectively.")

        if any(w in question_lower for w in ["where do you see yourself", "5 years", "future plans"]):
            return ("I see myself growing professionally, taking on more responsibilities, "
                    "and making meaningful contributions to the organization.")

        if any(w in question_lower for w in ["salary", "compensation", "package"]):
            return ("I'm open to discussing compensation based on the role's responsibilities. "
                    "I'm primarily focused on finding the right fit and long-term growth opportunity.")

        if "python" in question_lower:
            return ("Python is a versatile, readable programming language excellent for automation, "
                    "data analysis, web development, and AI. Its rich library ecosystem makes it very powerful.")

        if "api" in question_lower:
            return ("An API is an Application Programming Interface that allows different software systems "
                    "to communicate using standard request and response formats.")

        if "machine learning" in question_lower or "ai" in question_lower:
            return ("Machine learning is a subset of AI where systems learn from data to improve performance "
                    "without being explicitly programmed. It powers recommendations, voice assistants, and more.")

        return (f"For the question about '{question[:50]}': "
                "Structure your answer using the STAR method — Situation, Task, Action, Result. "
                "Be specific, confident, and relate it to your experience. You've got this, Sir!")

    def learn(self, trigger: str, response: str):
        if 'learned' not in self.knowledge.knowledge:
            self.knowledge.knowledge['learned'] = {}
        self.knowledge.knowledge['learned'][trigger.lower()] = response

    def remember(self, category: str, information: str):
        self.knowledge.knowledge.setdefault(category, [])
        self.knowledge.knowledge[category].append({
            "info": information,
            "added": datetime.now().isoformat()
        })

    def recall(self, category: str) -> Optional[str]:
        if category in self.knowledge.knowledge:
            items = self.knowledge.knowledge[category]
            if items:
                last = items[-1]
                return last.get("info", last) if isinstance(last, dict) else last
        return None