"""Test command helpers."""

from __future__ import annotations


def local_test_commands() -> list[str]:
    return ["python -m pytest", "python -m compileall src tests"]
