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
                plan="Analyze the requirement and extract structured expectations.",
                act="Create a ParsedRequirements object.",
                reason="The jury expects an explicit understanding of the input.",
            )
        )
        return state
