import os
from typing import List, Optional

class TreePrinter:
    def __init__(self, ignore_list: Optional[List[str]] = None):
        self.ignore_list = ignore_list or ["__pycache__", ".git", ".venv"]
        self.output = []

    def print_tree(self, start_path: str) -> str:
        """Print directory tree structure."""
        self.output = [os.path.basename(os.path.abspath(start_path))]
        self._walk_directory(start_path)
        return "\n".join(self.output)

    def _walk_directory(self, start_path: str, prefix: str = "") -> None:
        """Recursively walk directory and build tree structure."""
        entries = sorted(os.scandir(start_path), key=lambda e: e.name)
        entries = [e for e in entries if e.name not in self.ignore_list]
        
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            self.output.append(f"{prefix}{connector}{entry.name}")
            
            if entry.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._walk_directory(entry.path, new_prefix)
