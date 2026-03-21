"""QA and DevOps agent."""

from __future__ import annotations

from ai_delivery.contracts import ReasoningStep


class QaDevopsAgent:
    name = "qa_devops"

    def run(self, state):  # noqa: ANN001
        checks = [
            "github workflows present",
            "pre-commit configured",
            "quality commands documented",
        ]
        state.run_metadata["quality_checks"] = checks
        state.reasoning_trace.append(
            ReasoningStep(
                stage=self.name,
                plan="Verifier l'outillage qualite et la CI.",
                act="Enregistrement des controles qualitatifs principaux.",
                reason="La demonstration doit montrer un pipeline de livraison complet.",
            )
        )
        return state
