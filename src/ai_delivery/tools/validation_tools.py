"""Validation helpers."""

from __future__ import annotations

from pathlib import Path


def missing_paths(paths: list[Path]) -> list[str]:
    return [str(path) for path in paths if not path.exists()]
