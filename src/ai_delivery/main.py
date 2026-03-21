"""Pipeline execution entry point."""

from __future__ import annotations

from ai_delivery.contracts.session_models import RunRequest
from ai_delivery.services.session_service import SessionService
from ai_delivery.settings import load_settings
from ai_delivery.state import DeliveryState


def run_pipeline(
    input_path: str,
    dry_run: bool = False,
    settings_path: str | None = None,
) -> DeliveryState:
    settings = load_settings(settings_path)
    session = SessionService(settings).start_run(
        RunRequest(
            input_path=input_path,
            dry_run=dry_run,
            interactive=False,
        )
    )
    return session.state
