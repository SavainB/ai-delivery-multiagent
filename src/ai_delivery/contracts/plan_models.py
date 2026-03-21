"""Planning contracts."""

from __future__ import annotations

from ai_delivery.utils.pydantic_compat import BaseModel, Field


class ModulePlan(BaseModel):
    name: str
    responsibilities: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)


class ProjectBlueprint(BaseModel):
    project_name: str
    architecture_style: str
    modules: list[ModulePlan] = Field(default_factory=list)
    milestones: list[str] = Field(default_factory=list)
    quality_gates: list[str] = Field(default_factory=list)
