"""Helpers for CI artifact descriptions."""

from __future__ import annotations


def default_quality_steps() -> list[str]:
    return ["uv sync --all-extras", "ruff check .", "ruff format --check .", "pytest"]
