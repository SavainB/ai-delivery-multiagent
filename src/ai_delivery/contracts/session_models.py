"""Run session and intervention contracts."""

from __future__ import annotations

from typing import Any

from ai_delivery.state import DeliveryState
from ai_delivery.utils.pydantic_compat import BaseModel, Field


class RunRequest(BaseModel):
    input_path: str | None = None
    raw_input: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = False
    interactive: bool = False
    stop_after_stage: str | None = None


class InterventionRequest(BaseModel):
    state_field: str
    patch: dict[str, Any] = Field(default_factory=dict)
    resume: bool = True


class RunSession(BaseModel):
    run_id: str
    status: str
    dry_run: bool = False
    interactive: bool = False
    current_stage: str | None = None
    next_stage: str | None = None
    completed_stages: list[str] = Field(default_factory=list)
    state: DeliveryState
    session_path: str
