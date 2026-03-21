"""Graph state."""

from __future__ import annotations

from typing import Any

from ai_delivery.contracts import (
    ArchitectureDesign,
    GeneratedAppManifest,
    ParsedRequirements,
    ProjectBlueprint,
    ProjectInput,
    ReasoningStep,
    ValidationReport,
)
from ai_delivery.utils.pydantic_compat import BaseModel, Field


class DeliveryState(BaseModel):
    raw_input: ProjectInput | None = None
    parsed_requirements: ParsedRequirements | None = None
    project_blueprint: ProjectBlueprint | None = None
    architecture_design: ArchitectureDesign | None = None
    generated_files_index: GeneratedAppManifest | None = None
    c4_docs: list[dict[str, Any]] = Field(default_factory=list)
    validation_report: ValidationReport | None = None
    reasoning_trace: list[ReasoningStep] = Field(default_factory=list)
    run_metadata: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
