"""Settings loading."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from ai_delivery.utils.paths import project_root
from ai_delivery.utils.pydantic_compat import BaseModel


class AppSettings(BaseModel):
    project_name: str
    environment: str
    provider: str
    output_dir: str
    workspace_dir: str
    prompts_dir: str
    docs_dir: str
    templates_dir: str
    default_dry_run: bool = False
    trace_level: str = "detailed"

    @property
    def root_dir(self) -> Path:
        return project_root()

    @property
    def output_path(self) -> Path:
        return self.root_dir / self.output_dir

    @property
    def workspace_path(self) -> Path:
        return self.root_dir / self.workspace_dir

    @property
    def prompts_path(self) -> Path:
        return self.root_dir / self.prompts_dir

    @property
    def docs_path(self) -> Path:
        return self.root_dir / self.docs_dir

    @property
    def templates_path(self) -> Path:
        return self.root_dir / self.templates_dir


def load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return data


def load_settings(path: str | None = None) -> AppSettings:
    configured = path or os.getenv("AI_DELIVERY_CONFIG", "configs/settings.yaml")
    settings_path = project_root() / configured
    data = load_yaml_file(settings_path)
    return AppSettings.model_validate(data)
