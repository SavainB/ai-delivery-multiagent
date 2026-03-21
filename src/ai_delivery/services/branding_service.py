"""Branding configuration service."""

from __future__ import annotations

import os
from pathlib import Path

import yaml


class BrandingService:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def load(self, path: str | None = None) -> dict[str, str]:
        configured = path or os.getenv("AI_DELIVERY_BRAND", "configs/clients/demo_brand.yaml")
        file_path = self.root_dir / configured
        data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        return {str(key): str(value) for key, value in data.items()}
