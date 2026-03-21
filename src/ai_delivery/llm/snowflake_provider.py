"""Mock and Snowflake-oriented provider implementations."""

from __future__ import annotations

from typing import Any

from ai_delivery.contracts import (
    ArchitectureDesign,
    C4Document,
    ParsedRequirements,
    ProjectBlueprint,
    UserStory,
    ValidationReport,
)
from ai_delivery.llm.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    name = "mock"

    def generate_structured(self, prompt: str, schema: Any, context: dict[str, Any]) -> Any:
        prompt_lower = prompt.lower()
        if schema is ParsedRequirements:
            return ParsedRequirements(
                summary="Task management prototype for project teams.",
                user_stories=[
                    UserStory(
                        title="View tasks",
                        description="A user sees a filterable dashboard.",
                        acceptance_criteria=["visible list", "status filter", "priority filter"],
                    ),
                    UserStory(
                        title="Manage a task",
                        description="A user creates, updates, or deletes a task.",
                        acceptance_criteria=["creation", "edition", "deletion"],
                    ),
                ],
                constraints=context.get("constraints", []),
                modules=["dashboard", "task_detail", "task_form", "api", "quality"],
                journeys=[
                    "identify with a simple username",
                    "open the dashboard",
                    "create a task",
                    "update the status",
                ],
                assumptions=["Demo mode favors local SQLite storage."],
            )
        if schema is ProjectBlueprint:
            return ProjectBlueprint(
                project_name="AI Delivery Multi-Agent",
                architecture_style="deterministic multi-agent generator",
                modules=[
                    {
                        "name": "generator-core",
                        "responsibilities": ["orchestration", "state", "prompts"],
                        "deliverables": ["plan", "traces", "reports"],
                    },
                    {
                        "name": "generated-app",
                        "responsibilities": ["fastapi backend", "react frontend"],
                        "deliverables": ["workspace app", "tests", "ci"],
                    },
                ],
                milestones=[
                    "requirement analysis",
                    "architecture design",
                    "application generation",
                    "final validation",
                ],
                quality_gates=["ruff check", "ruff format --check", "pytest"],
            )
        if schema is ArchitectureDesign:
            return ArchitectureDesign(
                overview=(
                    "Separated architecture between the Python generator "
                    "and the generated application."
                ),
                backend_components=[
                    "FastAPI app",
                    "task router",
                    "task service",
                    "sqlite repository",
                ],
                frontend_components=[
                    "dashboard page",
                    "task form",
                    "task detail",
                    "api client",
                ],
                data_entities=["Task", "UserContext"],
                decisions=[
                    "LangGraph for the agent workflow",
                    "Mermaid for C4 documentation",
                    "Abstract provider for Snowflake",
                ],
                c4_documents=[
                    C4Document(
                        name="context",
                        description="Context view",
                        mermaid="flowchart LR\n  User --> Generator\n  Generator --> App",
                        output_path="docs/c4-context.md",
                    ),
                ],
            )
        if schema is ValidationReport or "review" in prompt_lower:
            return ValidationReport(
                status="ready-for-demo",
                checks=[
                    "plan persisted",
                    "c4 docs generated",
                    "workspace scaffold generated",
                ],
                warnings=["Install uv, pydantic, pytest, and langgraph for full execution."],
                next_actions=[
                    "uv sync --all-extras",
                    ("python -m ai_delivery.cli run --input inputs/sample_spec.md"),
                ],
            )
        raise ValueError(f"Unsupported schema: {schema}")


class SnowflakeProvider(BaseLLMProvider):
    name = "snowflake"

    def __init__(self, fallback: BaseLLMProvider | None = None) -> None:
        self.fallback = fallback or MockLLMProvider()

    def generate_structured(self, prompt: str, schema: Any, context: dict[str, Any]) -> Any:
        return self.fallback.generate_structured(
            prompt=prompt,
            schema=schema,
            context=context,
        )
