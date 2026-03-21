"""Retry helper."""

from __future__ import annotations

from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry(operation: Callable[[], T], attempts: int = 2, delay_seconds: float = 0.0) -> T:
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if delay_seconds:
                sleep(delay_seconds)
    assert last_error is not None
    raise last_error
