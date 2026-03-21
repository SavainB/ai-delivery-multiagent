from ai_delivery.main import run_pipeline
from ai_delivery.settings import load_settings


def test_codegen_pipeline_generates_workspace_files() -> None:
    state = run_pipeline("inputs/sample_spec.md", dry_run=False)
    workspace = load_settings().workspace_path
    assert state.generated_files_index is not None
    assert (workspace / "backend" / "app" / "main.py").exists()
    assert (workspace / "frontend" / "src" / "App.jsx").exists()
