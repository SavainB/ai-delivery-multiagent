"""Input parsing service."""

from __future__ import annotations

import json
from pathlib import Path

from ai_delivery.contracts import ParsedRequirements, ProjectInput
from ai_delivery.llm.structured_output import generate_with_schema


class InputParser:
    def __init__(self, provider, prompt_loader) -> None:  # noqa: ANN001
        self.provider = provider
        self.prompt_loader = prompt_loader

    def read_input(self, input_path: Path, context_path: Path | None = None) -> ProjectInput:
        content = input_path.read_text(encoding="utf-8")
        context = {}
        if context_path and context_path.exists():
            context = json.loads(context_path.read_text(encoding="utf-8"))
        content_type = "json" if input_path.suffix == ".json" else "markdown"
        return ProjectInput(
            source_path=str(input_path),
            content=content,
            content_type=content_type,
            context=context,
        )

    def parse(self, project_input: ProjectInput) -> ParsedRequirements:
        prompt = self.prompt_loader.load_bundle(
            "shared/system_common.txt",
            "shared/output_contracts.txt",
            "agents/spec_analyst.txt",
            "tasks/analyze_input.txt",
        )
        constraints = self._extract_constraints(project_input.content)
        context = {
            "raw_input": project_input.content,
            "constraints": constraints,
            "context": project_input.context,
        }
        return generate_with_schema(self.provider, prompt, ParsedRequirements, context)

    @staticmethod
    def _extract_constraints(content: str) -> list[str]:
        lines = [line.strip("- ").strip() for line in content.splitlines()]
        return [
            line
            for line in lines
            if line and ("demo" in line.lower() or "architecture" in line.lower())
        ]
