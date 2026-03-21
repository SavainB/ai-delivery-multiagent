from ai_delivery.main import run_pipeline


def test_end_to_end_dry_run() -> None:
    state = run_pipeline("inputs/sample_spec.md", dry_run=True)
    assert state.project_blueprint is not None
    assert state.validation_report is not None
    assert state.generated_files_index is not None
