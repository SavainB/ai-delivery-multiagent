from ai_delivery.contracts.session_models import InterventionRequest, RunRequest
from ai_delivery.services.session_service import SessionService
from ai_delivery.settings import load_settings


def test_interactive_session_can_pause_patch_and_resume() -> None:
    service = SessionService(load_settings())
    session = service.start_run(
        RunRequest(
            input_path="inputs/sample_spec.md",
            dry_run=True,
            interactive=True,
        )
    )
    assert session.status == "waiting_for_intervention"
    assert session.next_stage == "architect"

    resumed = service.apply_intervention(
        session.run_id,
        InterventionRequest(
            state_field="parsed_requirements",
            patch={"summary": "Requirement summary edited by user"},
            resume=True,
        ),
    )
    assert resumed.status == "waiting_for_intervention"
    assert resumed.state.parsed_requirements is not None
    assert resumed.state.parsed_requirements.summary == "Requirement summary edited by user"
