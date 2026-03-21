"""Planning service."""

from __future__ import annotations

from ai_delivery.contracts import ParsedRequirements, ProjectBlueprint
from ai_delivery.llm.structured_output import generate_with_schema


class Planner:
    def __init__(self, provider, prompt_loader) -> None:  # noqa: ANN001
        self.provider = provider
        self.prompt_loader = prompt_loader

    def create_blueprint(self, requirements: ParsedRequirements) -> ProjectBlueprint:
        prompt = self.prompt_loader.load_bundle(
            "shared/system_common.txt",
            "agents/architect.txt",
            "tasks/design_architecture.txt",
        )
        return generate_with_schema(
            self.provider,
            prompt,
            ProjectBlueprint,
            {"requirements": requirements.model_dump()},
        )
