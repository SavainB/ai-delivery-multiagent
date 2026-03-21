"""Checkpoint serialization helpers."""

from __future__ import annotations

from pathlib import Path

from ai_delivery.utils.json_utils import dump_json


def write_checkpoint(path: Path, payload: dict) -> None:
    dump_json(path, payload)
