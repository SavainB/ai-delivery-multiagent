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
                plan="Generate the target application and its technical structure.",
                act="Render the backend and frontend templates into the workspace.",
                reason=("The topic requires tangible software artifacts, not only documentation."),
            )
        )
        return state
