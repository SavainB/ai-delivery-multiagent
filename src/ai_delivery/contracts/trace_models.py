"""Trace and validation contracts."""

from __future__ import annotations

from ai_delivery.utils.pydantic_compat import BaseModel, Field


class ReasoningStep(BaseModel):
    stage: str
    plan: str
    act: str
    reason: str


class ValidationReport(BaseModel):
    status: str
    checks: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
