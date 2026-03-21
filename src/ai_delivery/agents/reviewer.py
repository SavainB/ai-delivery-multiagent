"""Reviewer agent."""

from __future__ import annotations

from ai_delivery.contracts import ReasoningStep


class ReviewerAgent:
    name = "reviewer"

    def __init__(self, reporting_service, settings) -> None:  # noqa: ANN001
        self.reporting_service = reporting_service
        self.settings = settings

    def run(self, state):  # noqa: ANN001
        expected_paths = [
            self.settings.docs_path / "c4-context.md",
            self.settings.docs_path / "c4-container.md",
            self.settings.docs_path / "c4-component.md",
        ]
        if not bool(state.run_metadata.get("dry_run", False)):
            expected_paths.append(self.settings.workspace_path / "backend" / "app" / "main.py")
            expected_paths.append(self.settings.workspace_path / "frontend" / "src" / "App.jsx")
        state.validation_report = self.reporting_service.review(expected_paths)
        state.reasoning_trace.append(
            ReasoningStep(
                stage=self.name,
                plan="Valider la coherence globale des livrables.",
                act="Generation d'un rapport final.",
                reason="Le jury verifiera la coherence entre besoin, architecture, code et traces.",
            )
        )
        return state
