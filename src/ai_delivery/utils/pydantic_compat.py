"""Minimal Pydantic compatibility layer for environments without pydantic."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

try:
    from pydantic import BaseModel, Field  # type: ignore
except ImportError:

    class _FieldSpec:
        def __init__(self, default: Any = None, default_factory: Any = None) -> None:
            self.default = default
            self.default_factory = default_factory

    def Field(default: Any = None, default_factory: Any = None, **_: Any) -> Any:
        return _FieldSpec(default=default, default_factory=default_factory)

    class BaseModel:
        """Small subset of the Pydantic API used by this repository."""

        def __init__(self, **data: Any) -> None:
            annotations: dict[str, Any] = {}
            for cls in reversed(self.__class__.__mro__):
                annotations.update(getattr(cls, "__annotations__", {}))
            for name in annotations:
                if name in data:
                    value = data[name]
                else:
                    default = getattr(self.__class__, name, None)
                    if isinstance(default, _FieldSpec):
                        if default.default_factory is not None:
                            value = default.default_factory()
                        else:
                            value = deepcopy(default.default)
                    else:
                        value = deepcopy(default)
                setattr(self, name, value)

        @classmethod
        def model_validate(cls, value: Any) -> BaseModel:
            if isinstance(value, cls):
                return value
            if isinstance(value, dict):
                return cls(**value)
            raise TypeError(f"Cannot validate {type(value)!r} into {cls.__name__}")

        @classmethod
        def model_validate_json(cls, payload: str) -> BaseModel:
            return cls.model_validate(json.loads(payload))

        def model_dump(self) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in self.__dict__.items():
                result[key] = self._dump_value(value)
            return result

        def model_dump_json(self, **kwargs: Any) -> str:
            return json.dumps(self.model_dump(), **kwargs)

        @classmethod
        def model_json_schema(cls) -> dict[str, Any]:
            return {"title": cls.__name__}

        @staticmethod
        def _dump_value(value: Any) -> Any:
            if isinstance(value, BaseModel):
                return value.model_dump()
            if isinstance(value, list):
                return [BaseModel._dump_value(item) for item in value]
            if isinstance(value, dict):
                return {key: BaseModel._dump_value(item) for key, item in value.items()}
            return value
