import os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FileStats:
    total_files: int = 0
    total_lines: int = 0
    total_chars: int = 0

class ContentWriter:
    def __init__(self, ignore_list: Optional[List[str]] = None):
        self.ignore_list = ignore_list or ["__pycache__", ".git", ".venv"]
        self.stats = FileStats()
        self.content = []

    def process_directory(self, start_path: str) -> str:
        """Process directory and return formatted content."""
        self._walk_directory(start_path)
        return "\n\n".join(self.content)

    def _walk_directory(self, start_path: str) -> None:
        """Walk through directory and process files."""
        for root, dirs, files in os.walk(start_path):
            # Remove ignored directories
            dirs[:] = [d for d in sorted(dirs) if d not in self.ignore_list]
            
            for file in sorted(files):
                file_path = os.path.join(root, file)
                self.stats.total_files += 1
                self._process_file(file_path)

    def _process_file(self, file_path: str) -> None:
        """Process individual file and update statistics."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.stats.total_lines += content.count("\n") + 1
                self.stats.total_chars += len(content)
                self.content.append(f"{self.stats.total_files}. {file_path}\n{content}")
        except (UnicodeDecodeError, IOError) as e:
            self.content.append(f"{self.stats.total_files}. {file_path}\nError reading file: {e}")
