from ai_delivery.settings import load_settings


def test_load_settings_reads_default_file() -> None:
    settings = load_settings()
    assert settings.project_name == "AI Delivery Multi-Agent"
    assert settings.workspace_dir == "workspace/generated_app"
