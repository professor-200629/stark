"""
STARK File Explorer - File and Folder Management
"""

import os
import sys
import shutil
import subprocess
from typing import Optional, List, Dict


class FileExplorer:
    """File system navigation and management"""

    def __init__(self):
        self.current_directory = os.path.expanduser("~")
        self.history = []
        self.max_history = 50
        print("[FileExplorer] Initialized.")

    # ========== NAVIGATION ==========

    def navigate_to(self, path: str) -> str:
        try:
            if path == "~" or path.lower() == "home":
                path = os.path.expanduser("~")
            elif path.lower() == "desktop":
                path = os.path.expanduser("~/Desktop")
            elif path.lower() == "documents":
                path = os.path.expanduser("~/Documents")
            elif path.lower() == "downloads":
                path = os.path.expanduser("~/Downloads")
            elif path.lower() == "pictures":
                path = os.path.expanduser("~/Pictures")
            elif path.lower() == "music":
                path = os.path.expanduser("~/Music")
            elif path.lower() == "videos":
                path = os.path.expanduser("~/Videos")

            if not os.path.isabs(path):
                path = os.path.join(self.current_directory, path)

            path = os.path.abspath(path)

            if os.path.isdir(path):
                self.history.append(self.current_directory)
                if len(self.history) > self.max_history:
                    self.history.pop(0)
                self.current_directory = path
                return f"Sir, now in: {path}"

            return f"Sir, '{path}' is not a valid directory."

        except Exception as e:
            return f"Sir, error navigating: {e}"

    def go_back(self) -> str:
        if self.history:
            self.current_directory = self.history.pop()
            return f"Sir, back to: {self.current_directory}"
        return "Sir, no previous directory in history."

    def go_up(self) -> str:
        parent = os.path.dirname(self.current_directory)
        if parent and parent != self.current_directory:
            self.history.append(self.current_directory)
            self.current_directory = parent
            return f"Sir, now in: {self.current_directory}"
        return "Sir, already at root directory."

    def get_current_path(self) -> str:
        return self.current_directory

    # ========== LISTING ==========

    def list_contents(self, path: str = None) -> str:
        target = path or self.current_directory

        try:
            if not os.path.isabs(target):
                target = os.path.join(self.current_directory, target)

            items = os.listdir(target)
            folders = []
            files = []

            for item in items:
                full_path = os.path.join(target, item)
                if os.path.isdir(full_path):
                    folders.append(item)
                else:
                    files.append(item)

            result = f"Sir, contents of {target}:\n\n"

            if folders:
                result += f"Folders ({len(folders)}):\n"
                for f in sorted(folders)[:15]:
                    result += f"  [DIR] {f}\n"
                if len(folders) > 15:
                    result += f"  ... and {len(folders) - 15} more\n"

            if files:
                result += f"\nFiles ({len(files)}):\n"
                for f in sorted(files)[:15]:
                    result += f"  {f}\n"
                if len(files) > 15:
                    result += f"  ... and {len(files) - 15} more\n"

            if not folders and not files:
                result += "  (empty directory)\n"

            return result

        except Exception as e:
            return f"Sir, error listing directory: {e}"

    # ========== SEARCH ==========

    def search_file(self, filename: str, search_path: str = None, max_results: int = 10) -> str:
        search_path = search_path or self.current_directory
        found = []

        try:
            for root, dirs, files in os.walk(search_path):
                for f in files:
                    if filename.lower() in f.lower():
                        found.append(os.path.join(root, f))
                        if len(found) >= max_results:
                            break
                if len(found) >= max_results:
                    break

            if found:
                result = f"Sir, found {len(found)} file(s):\n"
                for f in found:
                    result += f"  {f}\n"
                return result

            return f"Sir, no files matching '{filename}' found."

        except Exception as e:
            return f"Sir, error searching: {e}"

    # ========== CREATE ==========

    def create_folder(self, name: str, path: str = None) -> str:
        target = os.path.join(path or self.current_directory, name)

        try:
            os.makedirs(target, exist_ok=True)
            return f"Sir, created folder: {name}"
        except Exception as e:
            return f"Sir, error creating folder: {e}"

    def create_file(self, name: str, content: str = "", path: str = None) -> str:
        target = os.path.join(path or self.current_directory, name)

        try:
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Sir, created file: {name}"
        except Exception as e:
            return f"Sir, error creating file: {e}"

    # ========== DELETE ==========

    def delete_file(self, filepath: str) -> str:
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.current_directory, filepath)

        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
                return f"Sir, deleted file: {os.path.basename(filepath)}"
            return f"Sir, file not found: {filepath}"
        except Exception as e:
            return f"Sir, error deleting file: {e}"

    def delete_folder(self, folderpath: str) -> str:
        if not os.path.isabs(folderpath):
            folderpath = os.path.join(self.current_directory, folderpath)

        try:
            if os.path.isdir(folderpath):
                shutil.rmtree(folderpath)
                return f"Sir, deleted folder: {os.path.basename(folderpath)}"
            return f"Sir, folder not found: {folderpath}"
        except Exception as e:
            return f"Sir, error deleting folder: {e}"

    # ========== COPY & MOVE ==========

    def copy_file(self, source: str, destination: str) -> str:
        if not os.path.isabs(source):
            source = os.path.join(self.current_directory, source)
        if not os.path.isabs(destination):
            destination = os.path.join(self.current_directory, destination)

        try:
            shutil.copy2(source, destination)
            return f"Sir, copied {os.path.basename(source)} to {destination}"
        except Exception as e:
            return f"Sir, error copying file: {e}"

    def move_file(self, source: str, destination: str) -> str:
        if not os.path.isabs(source):
            source = os.path.join(self.current_directory, source)
        if not os.path.isabs(destination):
            destination = os.path.join(self.current_directory, destination)

        try:
            shutil.move(source, destination)
            return f"Sir, moved {os.path.basename(source)} to {destination}"
        except Exception as e:
            return f"Sir, error moving file: {e}"

    def rename(self, old_name: str, new_name: str) -> str:
        old_path = os.path.join(self.current_directory, old_name)
        new_path = os.path.join(self.current_directory, new_name)

        try:
            os.rename(old_path, new_path)
            return f"Sir, renamed {old_name} to {new_name}"
        except Exception as e:
            return f"Sir, error renaming: {e}"

    # ========== OPEN ==========

    def open_in_explorer(self, path: str = None) -> str:
        target = path or self.current_directory

        try:
            if os.name == 'nt':
                subprocess.Popen(f'explorer "{target}"')
            elif os.name == 'posix':
                subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', target])
            return f"Sir, opened File Explorer at {target}"
        except Exception as e:
            return f"Sir, error opening explorer: {e}"

    def open_file(self, filepath: str) -> str:
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.current_directory, filepath)

        try:
            if os.path.isfile(filepath):
                if os.name == 'nt':
                    os.startfile(filepath)
                else:
                    subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', filepath])
                return f"Sir, opened {os.path.basename(filepath)}"
            return f"Sir, file not found: {filepath}"
        except Exception as e:
            return f"Sir, error opening file: {e}"

    # ========== INFO ==========

    def get_file_info(self, filepath: str) -> str:
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.current_directory, filepath)

        try:
            if not os.path.exists(filepath):
                return f"Sir, file not found: {filepath}"

            stat = os.stat(filepath)
            is_file = os.path.isfile(filepath)

            info = f"Sir, information for {os.path.basename(filepath)}:\n"
            info += f"  • Type: {'File' if is_file else 'Folder'}\n"
            info += f"  • Path: {filepath}\n"
            info += f"  • Size: {self._format_size(stat.st_size)}\n"

            from datetime import datetime
            info += f"  • Created: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M')}\n"
            info += f"  • Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')}\n"

            if is_file:
                ext = os.path.splitext(filepath)[1]
                info += f"  • Extension: {ext}\n"

            return info

        except Exception as e:
            return f"Sir, error getting file info: {e}"

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"