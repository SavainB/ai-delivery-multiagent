"""Filesystem helpers for deterministic artifact generation."""

from __future__ import annotations

import shutil
from pathlib import Path


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_tree(source: Path, target: Path) -> list[Path]:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return [path for path in target.rglob("*") if path.is_file()]


def render_template(content: str, context: dict[str, str]) -> str:
    rendered = content
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def list_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())
