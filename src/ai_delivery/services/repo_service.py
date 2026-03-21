"""Repository artifact persistence."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ai_delivery.tools.filesystem import ensure_directory
from ai_delivery.utils.json_utils import dump_json


class RepoService:
    def __init__(self, root_dir: Path, output_dir: Path) -> None:
        self.root_dir = root_dir
        self.output_dir = output_dir

    def prepare_output_dirs(self) -> None:
        for name in ("runs", "traces", "plans", "c4"):
            ensure_directory(self.output_dir / name)

    def create_run_id(self) -> str:
        return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    def write_plan(self, run_id: str, payload: dict[str, Any]) -> Path:
        path = self.output_dir / "plans" / f"{run_id}-blueprint.json"
        dump_json(path, payload)
        return path

    def write_trace(self, run_id: str, payload: list[dict[str, Any]]) -> Path:
        path = self.output_dir / "traces" / f"{run_id}-trace.json"
        dump_json(path, payload)
        return path

    def write_report(self, run_id: str, payload: dict[str, Any]) -> Path:
        path = self.output_dir / "runs" / f"{run_id}-report.json"
        dump_json(path, payload)
        return path
