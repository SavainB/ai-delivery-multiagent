from ai_delivery.main import run_pipeline
from ai_delivery.settings import load_settings


def test_c4_docs_are_generated() -> None:
    run_pipeline("inputs/sample_spec.md", dry_run=True)
    docs = load_settings().docs_path
    assert (docs / "c4-context.md").exists()
    assert (docs / "c4-container.md").exists()
    assert (docs / "c4-component.md").exists()
