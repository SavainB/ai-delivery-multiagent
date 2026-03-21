"""Architect agent."""

from __future__ import annotations

from ai_delivery.contracts import ReasoningStep


class ArchitectAgent:
    name = "architect"

    def __init__(self, planner, architecture_service, c4_service) -> None:  # noqa: ANN001
        self.planner = planner
        self.architecture_service = architecture_service
        self.c4_service = c4_service

    def run(self, state):  # noqa: ANN001
        assert state.parsed_requirements is not None
        state.project_blueprint = self.planner.create_blueprint(state.parsed_requirements)
        state.architecture_design = self.architecture_service.design(
            state.parsed_requirements,
            state.project_blueprint,
        )
        state.c4_docs = self.c4_service.generate(state.architecture_design)
        state.reasoning_trace.append(
            ReasoningStep(
                stage=self.name,
                plan="Transformer les exigences en architecture et vues C4.",
                act="Production du blueprint, des decisions et des diagrammes.",
                reason="La solution doit rester defendable et coherente avec le brief IBM.",
            )
        )
        return state
