"""Template helpers."""

from __future__ import annotations

from pathlib import Path

from ai_delivery.tools.filesystem import list_files


def template_manifest(root: Path) -> list[str]:
    return [str(path.relative_to(root)) for path in list_files(root)]
