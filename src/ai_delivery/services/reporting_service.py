"""Reporting and validation service."""

from __future__ import annotations

from pathlib import Path

from ai_delivery.contracts import ValidationReport
from ai_delivery.llm.structured_output import generate_with_schema
from ai_delivery.tools.validation_tools import missing_paths


class ReportingService:
    def __init__(self, provider, prompt_loader, settings) -> None:  # noqa: ANN001
        self.provider = provider
        self.prompt_loader = prompt_loader
        self.settings = settings

    def review(self, expected_paths: list[Path]) -> ValidationReport:
        prompt = self.prompt_loader.load_bundle(
            "shared/system_common.txt",
            "agents/reviewer.txt",
        )
        report = generate_with_schema(
            self.provider,
            prompt,
            ValidationReport,
            {"expected_paths": [str(path) for path in expected_paths]},
        )
        missing = missing_paths(expected_paths)
        if missing:
            report.status = "incomplete"
            report.warnings.extend([f"Missing path: {path}" for path in missing])
        report.checks.append("review completed")
        return report
