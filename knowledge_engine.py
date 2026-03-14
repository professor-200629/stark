"""
STARK Knowledge Engine - Built-in knowledge database
Massive internal knowledge for offline operation
"""

import json
import os
import random
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config


class KnowledgeEngine:
    """
    Comprehensive knowledge base for STARK
    Contains greetings, facts, code templates, and more
    """

    def __init__(self):
        self.knowledge = self._load_knowledge()
        self._build_extended_knowledge()
        print("[KnowledgeEngine] Loaded with extensive knowledge base.")

    def _load_knowledge(self):
        """Load knowledge from JSON file"""
        try:
            if os.path.exists(config.KNOWLEDGE_FILE):
                with open(config.KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[KnowledgeEngine] Could not load knowledge file: {e}")
        return {}

    def _build_extended_knowledge(self):
        """Build massive internal knowledge databases"""

        # ==================== MATH KNOWLEDGE ====================
        self.math_knowledge = {
            "addition": "Addition is combining two or more numbers. Example: 5 + 3 = 8",
            "subtraction": "Subtraction is taking one number away from another. Example: 10 - 4 = 6",
            "multiplication": "Multiplication is repeated addition. Example: 4 × 3 = 12",
            "division": "Division is splitting into equal parts. Example: 12 ÷ 3 = 4",
            "algebra": "Algebra uses letters (variables) to represent unknown numbers. Example: x + 5 = 10, so x = 5",
            "geometry": "Geometry is the study of shapes, sizes, positions, and properties of space.",
            "calculus": "Calculus studies rates of change (derivatives) and accumulation (integrals).",
            "trigonometry": "Trigonometry deals with relationships between angles and sides of triangles. Key functions: sin, cos, tan.",
            "statistics": "Statistics is collecting, analyzing, and interpreting data. Includes mean, median, mode.",
            "probability": "Probability measures how likely an event is to occur. Ranges from 0 (impossible) to 1 (certain).",
            "pythagoras": "Pythagorean theorem: In a right triangle, a² + b² = c² where c is the hypotenuse.",
            "pi": "Pi (π) is approximately 3.14159. It's the ratio of a circle's circumference to its diameter.",
            "fibonacci": "Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21... Each number is the sum of the two before it.",
            "prime numbers": "Prime numbers are numbers greater than 1 that are only divisible by 1 and themselves.",
        }

        # ==================== SCIENCE KNOWLEDGE ====================
        self.science_knowledge = {
            "gravity": "Gravity is the force that attracts objects toward each other. On Earth, it pulls everything at 9.8 m/s².",
            "atom": "An atom is the smallest unit of matter. It has protons, neutrons (nucleus) and electrons (orbiting).",
            "photosynthesis": "Photosynthesis is how plants make food using sunlight, water, and CO₂.",
            "evolution": "Evolution is change in organisms over generations through natural selection. Darwin proposed this.",
            "dna": "DNA carries genetic instructions. It has a double helix structure.",
            "solar system": "Our solar system has 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.",
            "speed of light": "Speed of light is ~300,000 km/s. Nothing travels faster.",
            "newton laws": "Newton's Laws: 1) Inertia, 2) F=ma, 3) Action-Reaction",
            "electricity": "Electricity is flow of electrons. Ohm's Law: V = I × R",
            "relativity": "Einstein's Relativity: E=mc². Gravity curves spacetime.",
        }

        # ==================== HISTORY KNOWLEDGE ====================
        self.history_knowledge = {
            "world war 1": "World War 1 (1914-1918) was triggered by Archduke Franz Ferdinand's assassination. 17 million died.",
            "world war 2": "World War 2 (1939-1945) was the deadliest conflict. 70-85 million died. Ended with Hiroshima/Nagasaki.",
            "indian independence": "India gained independence on August 15, 1947. Gandhi led the non-violent movement.",
            "moon landing": "July 20, 1969: Neil Armstrong became first human on Moon. 'One small step for man...'",
            "mahatma gandhi": "Gandhi (1869-1948) led India's independence using non-violent civil disobedience.",
            "cold war": "Cold War (1947-1991) was tension between USA and USSR. Ended with Soviet Union's fall.",
        }

        # ==================== CODING KNOWLEDGE ====================
        self.coding_knowledge = {
            "variable": "A variable stores data. Python: x = 5. JavaScript: let x = 5;",
            "function": "A function is reusable code. Python: def greet(): print('Hello')",
            "loop": "Loops repeat code. for i in range(5): print(i)",
            "if statement": "If checks conditions: if x > 5: print('big')",
            "list": "List stores multiple items: my_list = [1, 2, 3]",
            "dictionary": "Dictionary stores key-value pairs: my_dict = {'name': 'John', 'age': 25}",
            "class": "Class is a blueprint for objects: class Dog: def bark(self): print('Woof!')",
            "api": "API allows software communication. REST uses GET, POST, PUT, DELETE.",
            "git": "Git is version control. Commands: git init, add, commit, push, pull",
            "database": "Databases store data. SQL uses tables (MySQL), NoSQL uses documents (MongoDB).",
            "recursion": "Recursion is when a function calls itself.",
            "oop": "OOP has: Encapsulation, Inheritance, Polymorphism, Abstraction",
        }

        # ==================== HEALTH KNOWLEDGE ====================
        self.health_knowledge = {
            "hair fall": "Sir, reduce hair fall: oil regularly, eat protein, avoid hot water, reduce stress, take biotin.",
            "headache": "Sir, for headache: drink water, rest in dark room, cold compress, massage temples, take screen breaks.",
            "eye strain": "Sir, follow 20-20-20 rule: every 20 mins, look 20 feet away for 20 seconds.",
            "back pain": "Sir, maintain posture, use lumbar support, stretch every 30 mins, strengthen core.",
            "sleep": "Sir, for better sleep: consistent schedule, no screens before bed, dark cool room, avoid caffeine after 4 PM.",
            "stress": "Sir, manage stress: deep breathing, exercise, talk to someone, take breaks, listen to music.",
            "cold": "Sir, for cold: rest, warm fluids, gargle salt water, steam inhalation, vitamin C.",
            "digestion": "Sir, better digestion: eat slowly, drink water, fiber-rich foods, walk after meals.",
            "skin care": "Sir, for skin: drink 8 glasses water, use sunscreen, wash face twice, eat fruits.",
            "weight loss": "Sir, weight loss: calorie deficit, more protein, exercise, avoid sugar, sleep well.",
            "immunity": "Sir, boost immunity: vitamin C, sleep, exercise, turmeric, ginger, probiotics.",
        }

        # ==================== CODE TEMPLATES ====================
        self.code_templates = {
            "calculator": '''# Simple Calculator
def calculator():
    print("=== STARK Calculator ===")
    while True:
        try:
            num1 = float(input("First number: "))
            op = input("Operation (+, -, *, /): ")
            num2 = float(input("Second number: "))

            if op == '+': result = num1 + num2
            elif op == '-': result = num1 - num2
            elif op == '*': result = num1 * num2
            elif op == '/': result = num1 / num2 if num2 != 0 else "Error"
            else: result = "Invalid"

            print(f"Result: {result}")
            if input("Continue? (y/n): ").lower() != 'y': break
        except: print("Invalid input!")

calculator()''',

            "todo list": '''# Todo List
class TodoList:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append({"task": task, "done": False})
        print(f"Added: {task}")

    def show(self):
        for i, t in enumerate(self.tasks, 1):
            status = "✓" if t["done"] else "✗"
            print(f"{i}. [{status}] {t['task']}")

todo = TodoList()
while True:
    print("\\n1. Add  2. Complete  3. Show  4. Exit")
    c = input("Choice: ")
    if c == "1": todo.add(input("Task: "))
    elif c == "2": todo.tasks[int(input("Number: "))-1]["done"] = True
    elif c == "3": todo.show()
    elif c == "4": break''',

            "password generator": '''# Password Generator
import random, string

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

length = int(input("Password length: ") or 16)
print(f"Password: {generate_password(length)}")''',

            "web scraper": '''# Web Scraper
import requests
from bs4 import BeautifulSoup

url = input("Enter URL: ")
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

for script in soup(["script", "style"]):
    script.decompose()

text = soup.get_text()
print(text[:2000])''',

            "guessing game": '''# Guessing Game
import random

secret = random.randint(1, 100)
attempts = 0

print("I'm thinking of 1-100...")
while True:
    guess = int(input("Guess: "))
    attempts += 1
    if guess < secret: print("Too low!")
    elif guess > secret: print("Too high!")
    else:
        print(f"Correct! {attempts} attempts!")
        break''',
        }

    # ==================== PUBLIC METHODS ====================

    def get_greeting(self, text: str) -> str:
        greetings = self.knowledge.get('greetings', {})
        text_lower = text.lower().strip()
        for key, response in greetings.items():
            if key in text_lower:
                return response
        return None

    def get_about(self, text: str) -> str:
        about = self.knowledge.get('about', {})
        text_lower = text.lower().strip()
        for key, response in about.items():
            if key in text_lower:
                return response
        return None

    def get_health_tip(self) -> str:
        tips = self.knowledge.get('health_tips', [])
        if tips:
            return random.choice(tips)
        return "Sir, stay healthy: drink water, exercise, sleep well, eat vegetables."

    def get_motivation(self) -> str:
        quotes = self.knowledge.get('motivation', [])
        if quotes:
            return random.choice(quotes)
        return "Sir, you're capable of amazing things. Keep going!"

    def get_health_advice(self, text: str) -> str:
        text_lower = text.lower()
        for key, advice in self.health_knowledge.items():
            if key in text_lower:
                return advice
        return None

    def get_subject_info(self, text: str) -> str:
        text_lower = text.lower()

        # Check math
        for key, info in self.math_knowledge.items():
            if key in text_lower:
                return f"Sir, {info}"

        # Check science
        for key, info in self.science_knowledge.items():
            if key in text_lower:
                return f"Sir, {info}"

        # Check history
        for key, info in self.history_knowledge.items():
            if key in text_lower:
                return f"Sir, {info}"

        # Check coding
        for key, info in self.coding_knowledge.items():
            if key in text_lower:
                return f"Sir, {info}"

        # Check subjects in knowledge file
        subjects = self.knowledge.get('subjects', {})
        for key, info in subjects.items():
            if key in text_lower:
                return f"Sir, {info}"

        # Check general knowledge section
        general = self.knowledge.get('general_knowledge', {})
        for key, info in general.items():
            if key in text_lower:
                return info

        # Check cooking section
        cooking = self.knowledge.get('cooking', {})
        for key, info in cooking.items():
            if key in text_lower:
                return info

        return None

    def get_code_template(self, text: str) -> str:
        text_lower = text.lower()

        for key, template in self.code_templates.items():
            if key in text_lower:
                return template

        templates = self.knowledge.get('code_templates', {})
        for key, template in templates.items():
            if key in text_lower:
                return template

        return None

    def get_error_help(self, text: str) -> str:
        errors = self.knowledge.get('error_help', {})
        text_lower = text.lower()

        for key, help_text in errors.items():
            if key in text_lower:
                return help_text

        return None

    def search_all_knowledge(self, query: str) -> str:
        """Search all knowledge sources"""
        result = self.get_subject_info(query)
        if result:
            return result

        result = self.get_health_advice(query)
        if result:
            return result

        learned = self.knowledge.get('learned', {})
        for key, response in learned.items():
            if key in query.lower():
                return response

        return None