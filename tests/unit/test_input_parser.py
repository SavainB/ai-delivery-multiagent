from pathlib import Path

from ai_delivery.llm.prompt_loader import PromptLoader
from ai_delivery.llm.snowflake_provider import MockLLMProvider
from ai_delivery.services.input_parser import InputParser
from ai_delivery.settings import load_settings


def test_input_parser_reads_and_parses_spec() -> None:
    settings = load_settings()
    parser = InputParser(MockLLMProvider(), PromptLoader(settings))
    project_input = parser.read_input(Path("inputs/sample_spec.md"))
    parsed = parser.parse(project_input)
    assert parsed.summary
    assert parsed.modules
