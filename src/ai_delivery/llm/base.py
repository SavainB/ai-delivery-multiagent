"""Provider abstraction."""

from __future__ import annotations

from typing import Any


class BaseLLMProvider:
    """Simple provider protocol."""

    name = "base"

    def generate_structured(self, prompt: str, schema: Any, context: dict[str, Any]) -> Any:
        raise NotImplementedError
