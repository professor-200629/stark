"""
STARK Code Brain - Code Analysis, Debugging & Generation
"""

import re
import os
from typing import Optional, List, Dict, Tuple

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class CodeBrain:
    """Specialized brain for code-related tasks"""

    def __init__(self):
        self.gemini_model = None
        self.use_gemini = False
        self._init_ai()

        self.language_patterns = {
            'python': [r'def\s+\w+\s*\(', r'import\s+\w+', r'from\s+\w+\s*import'],
            'javascript': [r'function\s+\w+\s*\(', r'const\s+\w+\s*=', r'console\.log'],
            'java': [r'public\s+class\s+\w+', r'System\.out\.println'],
            'html': [r'<!DOCTYPE', r'<html', r'<head>', r'<body>'],
            'css': [r'\{\s*[\w-]+\s*:', r'@media'],
            'sql': [r'SELECT\s+', r'FROM\s+', r'WHERE\s+'],
        }

    def _init_ai(self):
        if GEMINI_AVAILABLE and config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.use_gemini = True
                print("[CodeBrain] Gemini AI connected!")
            except Exception as e:
                print(f"[CodeBrain] Gemini error: {e}")
        else:
            print("[CodeBrain] Running in local mode.")

    def detect_language(self, code: str = None, filepath: str = None) -> str:
        if filepath:
            ext = os.path.splitext(filepath)[1].lower()
            extension_map = {
                '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                '.java': 'java', '.cpp': 'cpp', '.c': 'c',
                '.html': 'html', '.htm': 'html', '.css': 'css',
                '.sql': 'sql', '.json': 'json',
            }
            if ext in extension_map:
                return extension_map[ext]

        if code:
            for lang, patterns in self.language_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, code, re.IGNORECASE):
                        return lang
        return 'unknown'

    def analyze(self, code: str, language: str = None) -> Dict:
        if not language:
            language = self.detect_language(code=code)

        analysis = {
            'language': language,
            'lines': len(code.split('\n')),
            'characters': len(code),
            'functions': [],
            'classes': [],
            'imports': [],
            'errors': [],
            'warnings': [],
            'suggestions': []
        }

        if language == 'python':
            analysis.update(self._analyze_python(code))

        return analysis

    def _analyze_python(self, code: str) -> Dict:
        result = {'functions': [], 'classes': [], 'imports': [], 'errors': [], 'warnings': [], 'suggestions': []}

        lines = code.split('\n')

        # Find functions
        for i, line in enumerate(lines, 1):
            func_match = re.match(r'\s*def\s+(\w+)\s*\((.*?)\)\s*:', line)
            if func_match:
                result['functions'].append({'name': func_match.group(1), 'params': func_match.group(2), 'line': i})

        # Find classes
        for i, line in enumerate(lines, 1):
            class_match = re.match(r'\s*class\s+(\w+)', line)
            if class_match:
                result['classes'].append({'name': class_match.group(1), 'line': i})

        # Check bracket balance
        if code.count('(') != code.count(')'):
            result['errors'].append({'message': f'Parenthesis mismatch'})
        if code.count('[') != code.count(']'):
            result['errors'].append({'message': f'Bracket mismatch'})
        if code.count('{') != code.count('}'):
            result['errors'].append({'message': f'Brace mismatch'})

        return result

    def full_analysis(self, code: str, language: str = None) -> str:
        analysis = self.analyze(code, language)
        lang = analysis['language']

        report = f"Sir, here's my analysis of your {lang} code:\n\n"
        report += f"Language: {lang}\n"
        report += f"Lines: {analysis['lines']}\n"
        report += f"Characters: {analysis['characters']}\n\n"

        if analysis.get('functions'):
            report += f"Functions ({len(analysis['functions'])}):\n"
            for func in analysis['functions']:
                report += f"  • {func['name']}() - line {func['line']}\n"
            report += "\n"

        if analysis.get('classes'):
            report += f"Classes ({len(analysis['classes'])}):\n"
            for cls in analysis['classes']:
                report += f"  • {cls['name']} - line {cls['line']}\n"
            report += "\n"

        if analysis.get('errors'):
            report += f"Errors ({len(analysis['errors'])}):\n"
            for err in analysis['errors']:
                report += f"  ❌ {err['message']}\n"
            report += "\n"

        if not analysis.get('errors'):
            report += "✅ No obvious errors detected!\n"

        return report

    def generate_code(self, description: str, language: str = "python") -> str:
        if self.use_gemini and self.gemini_model:
            try:
                prompt = f"Generate complete, working {language} code for:\n{description}\nReturn ONLY code."
                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[CodeBrain] Gemini error: {e}")

        return self._generate_local(description, language)

    def _generate_local(self, description: str, language: str) -> str:
        desc_lower = description.lower()

        if "calculator" in desc_lower:
            return '''# Calculator
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Error"

print("Calculator ready!")'''

        if "hello" in desc_lower:
            return '''print("Hello, World!")'''

        return f'''# Code for: {description}
# Add your Gemini API key for better code generation

def main():
    """TODO: Implement {description}"""
    pass

if __name__ == "__main__":
    main()'''

    def explain_code(self, code: str, language: str = None) -> str:
        if not language:
            language = self.detect_language(code=code)

        analysis = self.analyze(code, language)

        explanation = f"Sir, this {language} code:\n"
        if analysis.get('functions'):
            explanation += f"Has {len(analysis['functions'])} function(s).\n"
        if analysis.get('classes'):
            explanation += f"Has {len(analysis['classes'])} class(es).\n"

        return explanation