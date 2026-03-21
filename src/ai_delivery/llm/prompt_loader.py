"""Prompt loading."""

from __future__ import annotations

from pathlib import Path

from ai_delivery.settings import AppSettings


class PromptLoader:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def load(self, relative_path: str) -> str:
        path = self.settings.prompts_path / relative_path
        return path.read_text(encoding="utf-8").strip()

    def load_bundle(self, *relative_paths: str) -> str:
        return "\n\n".join(self.load(path) for path in relative_paths)

    def exists(self, relative_path: str) -> bool:
        return (self.settings.prompts_path / relative_path).exists()

    def list_prompts(self) -> list[str]:
        root: Path = self.settings.prompts_path
        return sorted(str(path.relative_to(root)) for path in root.rglob("*.txt"))
