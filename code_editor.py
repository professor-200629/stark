"""
STARK Code Editor - File Editing and Code Management
"""

import os
import re
import shutil
from typing import Optional, List, Dict

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class CodeEditor:
    """Code editing capabilities for STARK"""

    def __init__(self, brain=None):
        self.brain = brain
        self.current_file = None
        self.current_content = ""
        self.file_history = []
        self.max_history = 20

    def read_file(self, filepath: str) -> Optional[str]:
        try:
            if not os.path.isabs(filepath):
                filepath = os.path.abspath(filepath)

            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            self.current_file = filepath
            self.current_content = content
            self._add_to_history(filepath, content)

            return content

        except Exception as e:
            print(f"[CodeEditor] Error reading file: {e}")
            return None

    def write_file(self, filepath: str, content: str) -> bool:
        try:
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            self.current_file = filepath
            self.current_content = content
            self._add_to_history(filepath, content)

            return True

        except Exception as e:
            print(f"[CodeEditor] Error writing file: {e}")
            return False

    def create_file(self, filepath: str, content: str = "") -> str:
        if os.path.exists(filepath):
            return f"Sir, file already exists: {filepath}"

        if self.write_file(filepath, content or "# New file\n"):
            return f"Sir, created file: {filepath}"
        return f"Sir, couldn't create file: {filepath}"

    def delete_file(self, filepath: str) -> str:
        try:
            if not os.path.exists(filepath):
                return f"Sir, file doesn't exist: {filepath}"

            os.remove(filepath)
            return f"Sir, deleted file: {filepath}"

        except Exception as e:
            return f"Sir, error deleting file: {e}"

    def open_file(self, filepath: str) -> str:
        content = self.read_file(filepath)

        if content is None:
            return f"Sir, couldn't find file: {filepath}"

        lines = len(content.split('\n'))
        size = len(content)

        return f"Sir, opened {filepath} ({lines} lines, {size} characters)."

    def edit_file(self, filepath: str, old_text: str, new_text: str) -> str:
        content = self.read_file(filepath)

        if content is None:
            return f"Sir, couldn't read file: {filepath}"

        if old_text not in content:
            return f"Sir, text not found: '{old_text[:50]}...'"

        new_content = content.replace(old_text, new_text, 1)

        if self.write_file(filepath, new_content):
            return f"Sir, edited {filepath}. Replaced '{old_text[:30]}...' with '{new_text[:30]}...'"

        return f"Sir, couldn't save changes to {filepath}"

    def append_to_file(self, filepath: str, text: str) -> str:
        content = self.read_file(filepath)

        if content is None:
            return self.create_file(filepath, text)

        new_content = content + '\n' + text

        if self.write_file(filepath, new_content):
            return f"Sir, appended text to {filepath}"

        return f"Sir, couldn't append to {filepath}"

    def insert_at_line(self, filepath: str, line_number: int, text: str) -> str:
        content = self.read_file(filepath)

        if content is None:
            return f"Sir, couldn't read file: {filepath}"

        lines = content.split('\n')

        if line_number < 1 or line_number > len(lines) + 1:
            return f"Sir, invalid line number: {line_number}"

        lines.insert(line_number - 1, text)
        new_content = '\n'.join(lines)

        if self.write_file(filepath, new_content):
            return f"Sir, inserted text at line {line_number}"

        return f"Sir, couldn't save changes"

    def delete_lines(self, filepath: str, start: int, end: int = None) -> str:
        content = self.read_file(filepath)

        if content is None:
            return f"Sir, couldn't read file: {filepath}"

        lines = content.split('\n')

        if end is None:
            end = start

        if start < 1 or end > len(lines):
            return f"Sir, invalid line range"

        del lines[start - 1:end]
        new_content = '\n'.join(lines)

        if self.write_file(filepath, new_content):
            return f"Sir, deleted lines {start} to {end}"

        return f"Sir, couldn't save changes"

    def search_in_file(self, filepath: str, search_text: str) -> List[Dict]:
        content = self.read_file(filepath)

        if content is None:
            return []

        results = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if search_text.lower() in line.lower():
                results.append({
                    "line": i,
                    "content": line.strip(),
                    "position": line.lower().find(search_text.lower())
                })

        return results

    def search_and_replace(self, filepath: str, search: str, replace: str, all_occurrences: bool = False) -> str:
        content = self.read_file(filepath)

        if content is None:
            return f"Sir, couldn't read file: {filepath}"

        if search not in content:
            return f"Sir, '{search}' not found in file"

        if all_occurrences:
            count = content.count(search)
            new_content = content.replace(search, replace)
        else:
            count = 1
            new_content = content.replace(search, replace, 1)

        if self.write_file(filepath, new_content):
            return f"Sir, replaced {count} occurrence(s) in {filepath}"

        return f"Sir, couldn't save changes"

    def get_file_info(self, filepath: str) -> Dict:
        if not os.path.exists(filepath):
            return {"error": "File not found"}

        stat = os.stat(filepath)
        content = self.read_file(filepath)

        return {
            "path": filepath,
            "name": os.path.basename(filepath),
            "extension": os.path.splitext(filepath)[1],
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 2),
            "lines": len(content.split('\n')) if content else 0,
            "modified": stat.st_mtime,
            "created": stat.st_ctime
        }

    def _add_to_history(self, filepath: str, content: str):
        self.file_history.append({
            "path": filepath,
            "content": content,
            "timestamp": __import__('time').time()
        })

        if len(self.file_history) > self.max_history:
            self.file_history.pop(0)

    def undo_last_change(self) -> str:
        if len(self.file_history) < 2:
            return "Sir, no changes to undo"

        previous = self.file_history[-2]

        if self.write_file(previous["path"], previous["content"]):
            self.file_history.pop()
            return f"Sir, undid changes to {previous['path']}"

        return "Sir, couldn't undo changes"