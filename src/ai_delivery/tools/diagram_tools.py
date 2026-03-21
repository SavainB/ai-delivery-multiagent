"""C4 Mermaid generation helpers."""

from __future__ import annotations


def build_context_diagram(app_name: str) -> str:
    return "\n".join(
        [
            "flowchart LR",
            f"  User[Business User] --> Generator[{app_name}]",
            "  Generator --> App[Generated Task App]",
            "  Generator --> Docs[C4 Documentation]",
        ]
    )


def build_container_diagram() -> str:
    return "\n".join(
        [
            "flowchart TB",
            "  CLI[CLI] --> Graph[Orchestrator]",
            "  Graph --> Agents[Agents]",
            "  Agents --> Services[Services]",
            "  Services --> Workspace[Generated App Workspace]",
        ]
    )


def build_component_diagram() -> str:
    return "\n".join(
        [
            "flowchart LR",
            "  Parser --> Planner",
            "  Planner --> Architect",
            "  Architect --> Codegen",
            "  Codegen --> Reviewer",
        ]
    )
