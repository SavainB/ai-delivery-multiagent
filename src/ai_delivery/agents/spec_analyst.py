"""Specification analyst agent."""

from __future__ import annotations

from ai_delivery.contracts import ReasoningStep


class SpecAnalystAgent:
    name = "spec_analyst"

    def __init__(self, input_parser) -> None:  # noqa: ANN001
        self.input_parser = input_parser

    def run(self, state):  # noqa: ANN001
        assert state.raw_input is not None
        state.parsed_requirements = self.input_parser.parse(state.raw_input)
        state.reasoning_trace.append(
            ReasoningStep(
                stage=self.name,
                plan="Analyser le besoin et extraire des exigences structurees.",
                act="Creation d'un objet ParsedRequirements.",
                reason="Le jury attend une comprehension explicite de l'entree.",
            )
        )
        return state
