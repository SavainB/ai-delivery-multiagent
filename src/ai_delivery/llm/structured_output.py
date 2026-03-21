"""Structured output parsing."""

from __future__ import annotations

from typing import Any

from ai_delivery.utils.retry import retry


def generate_with_schema(provider: Any, prompt: str, schema: Any, context: dict[str, Any]) -> Any:
    return retry(
        lambda: provider.generate_structured(
            prompt=prompt,
            schema=schema,
            context=context,
        )
    )
