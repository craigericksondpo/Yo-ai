# manifest_loader.py - utilities for loading and validating agent manifests
# yo_ai_main/shared/manifest_loader.py

import json
from pathlib import Path
from typing import Any, Dict


class ManifestLoader:
    """
    Loads agent manifests (agent cards) from disk.
    MVP version:
    - Reads JSON files
    - Returns dicts
    - Performs minimal validation
    """

    REQUIRED_FIELDS = ["id", "name", "capabilities", "lifespan"]

    @staticmethod
    def load_manifest(path: str | Path) -> Dict[str, Any]:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")

        data = json.loads(path.read_text())

        # Minimal validation
        for field in ManifestLoader.REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(f"Manifest missing required field: {field}")

        return data

    @staticmethod
    def load_all(directory: str | Path) -> Dict[str, Dict[str, Any]]:
        directory = Path(directory)
        manifests = {}

        for file in directory.glob("*.json"):
            manifest = ManifestLoader.load_manifest(file)
            manifests[manifest["id"]] = manifest

        return manifests