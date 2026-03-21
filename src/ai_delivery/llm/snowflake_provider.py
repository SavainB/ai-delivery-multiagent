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
                summary="Prototype de gestion de taches pour equipes projet.",
                user_stories=[
                    UserStory(
                        title="Consulter les taches",
                        description="Un utilisateur voit un tableau de bord filtrable.",
                        acceptance_criteria=["liste visible", "filtre statut", "filtre priorite"],
                    ),
                    UserStory(
                        title="Gerer une tache",
                        description="Un utilisateur cree, modifie ou supprime une tache.",
                        acceptance_criteria=["creation", "edition", "suppression"],
                    ),
                ],
                constraints=context.get("constraints", []),
                modules=["dashboard", "task_detail", "task_form", "api", "quality"],
                journeys=[
                    "s identifier simplement",
                    "consulter le dashboard",
                    "creer une tache",
                    "mettre a jour le statut",
                ],
                assumptions=["Le mode demo privilegie un stockage SQLite local."],
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
                    "analyse du besoin",
                    "conception architecture",
                    "generation application",
                    "validation finale",
                ],
                quality_gates=["ruff check", "ruff format --check", "pytest"],
            )
        if schema is ArchitectureDesign:
            return ArchitectureDesign(
                overview="Architecture separee entre generateur Python et application generee.",
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
                    "LangGraph pour le workflow agentique",
                    "Mermaid pour la documentation C4",
                    "Provider abstrait pour Snowflake",
                ],
                c4_documents=[
                    C4Document(
                        name="context",
                        description="Vue contexte",
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
                warnings=["Installer uv, pydantic, pytest et langgraph pour l'execution complete."],
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
