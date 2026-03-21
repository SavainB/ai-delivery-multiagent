from ai_delivery.llm.prompt_loader import PromptLoader
from ai_delivery.settings import load_settings


def test_prompt_loader_lists_prompts() -> None:
    loader = PromptLoader(load_settings())
    prompts = loader.list_prompts()
    assert "agents/spec_analyst.txt" in prompts
    assert loader.exists("shared/system_common.txt")
