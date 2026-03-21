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
                plan="Verify quality tooling and CI.",
                act="Record the main quality checks.",
                reason="The demo must show a complete delivery pipeline.",
            )
        )
        return state
