"""Developer agent."""

from __future__ import annotations

from ai_delivery.contracts import ReasoningStep


class DeveloperAgent:
    name = "developer"

    def __init__(self, codegen_service) -> None:  # noqa: ANN001
        self.codegen_service = codegen_service

    def run(self, state):  # noqa: ANN001
        dry_run = bool(state.run_metadata.get("dry_run", False))
        state.generated_files_index = self.codegen_service.generate_app(dry_run=dry_run)
        state.reasoning_trace.append(
            ReasoningStep(
                stage=self.name,
                plan="Generer l'application cible et sa structure technique.",
                act="Rendu des templates backend et frontend dans le workspace.",
                reason=(
                    "Le sujet demande des artefacts logiciels tangibles, "
                    "pas seulement de la documentation."
                ),
            )
        )
        return state
