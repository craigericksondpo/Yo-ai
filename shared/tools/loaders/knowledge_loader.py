# knowledge_loader.py - utilities for loading and validating knowledge bases

# yo_ai_main/shared/loaders/knowledge_loader.py

from pathlib import Path
from typing import Dict


class KnowledgeLoader:
    """
    Loads raw text files from a directory into a dictionary.
    Keys = filenames
    Values = file contents
    """

    def __init__(self, path: str):
        self.path = Path(path)

    def load_all(self) -> Dict[str, str]:
        knowledge: Dict[str, str] = {}

        if not self.path.exists():
            raise FileNotFoundError(f"Knowledge path does not exist: {self.path}")

        for file in self.path.glob("**/*"):
            if file.is_file():
                knowledge[file.name] = file.read_text(encoding="utf-8")

        return knowledge
