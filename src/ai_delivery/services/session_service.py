"""Session-based orchestration with user intervention checkpoints."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ai_delivery.agents.architect import ArchitectAgent
from ai_delivery.agents.developer import DeveloperAgent
from ai_delivery.agents.qa_devops import QaDevopsAgent
from ai_delivery.agents.reviewer import ReviewerAgent
from ai_delivery.agents.spec_analyst import SpecAnalystAgent
from ai_delivery.contracts.session_models import InterventionRequest, RunRequest, RunSession
from ai_delivery.graph.edges import DEFAULT_FLOW
from ai_delivery.llm.prompt_loader import PromptLoader
from ai_delivery.llm.snowflake_provider import MockLLMProvider, SnowflakeProvider
from ai_delivery.services.architecture_service import ArchitectureService
from ai_delivery.services.branding_service import BrandingService
from ai_delivery.services.c4_service import C4Service
from ai_delivery.services.codegen_service import CodegenService
from ai_delivery.services.input_parser import InputParser
from ai_delivery.services.planner import Planner
from ai_delivery.services.repo_service import RepoService
from ai_delivery.services.reporting_service import ReportingService
from ai_delivery.settings import AppSettings
from ai_delivery.state import DeliveryState
from ai_delivery.utils.json_utils import dump_json, load_json


def build_provider(name: str):
    if name == "snowflake":
        return SnowflakeProvider()
    return MockLLMProvider()


class SessionService:
    """Drive full or interactive runs and persist run sessions to disk."""

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self.provider = build_provider(settings.provider)
        self.prompt_loader = PromptLoader(settings)
        self.repo_service = RepoService(settings.root_dir, settings.output_path)
        self.repo_service.prepare_output_dirs()
        self.input_parser = InputParser(self.provider, self.prompt_loader)
        self.planner = Planner(self.provider, self.prompt_loader)
        self.architecture_service = ArchitectureService(
            self.provider,
            self.prompt_loader,
            settings,
        )
        self.c4_service = C4Service(self.architecture_service)
        self.branding_service = BrandingService(settings.root_dir)
        self.codegen_service = CodegenService(settings, self.branding_service)
        self.reporting_service = ReportingService(self.provider, self.prompt_loader, settings)
        self.agents = {
            "spec_analyst": SpecAnalystAgent(self.input_parser),
            "architect": ArchitectAgent(
                self.planner,
                self.architecture_service,
                self.c4_service,
            ),
            "developer": DeveloperAgent(self.codegen_service),
            "qa_devops": QaDevopsAgent(),
            "reviewer": ReviewerAgent(self.reporting_service, settings),
        }

    def start_run(self, request: RunRequest) -> RunSession:
        run_id = self.repo_service.create_run_id()
        state = DeliveryState()
        state.run_metadata = {
            "dry_run": request.dry_run,
            "interactive": request.interactive,
            "provider": self.provider.name,
            "settings": self.settings.model_dump(),
        }
        state.raw_input = self._build_project_input(request, run_id)
        return self._execute(
            run_id=run_id,
            state=state,
            start_index=0,
            completed_stages=[],
            interactive=request.interactive,
            stop_after_stage=request.stop_after_stage,
        )

    def resume_run(self, run_id: str) -> RunSession:
        session = self.load_session(run_id)
        if session.next_stage is None:
            raise ValueError("This run is already complete.")
        start_index = DEFAULT_FLOW.index(session.next_stage)
        return self._execute(
            run_id=run_id,
            state=session.state,
            start_index=start_index,
            completed_stages=session.completed_stages,
            interactive=session.interactive,
            stop_after_stage=None,
        )

    def apply_intervention(self, run_id: str, request: InterventionRequest) -> RunSession:
        session = self.load_session(run_id)
        state = self._patch_state(session.state, request.state_field, request.patch)
        updated_session = RunSession(
            run_id=session.run_id,
            status=session.status,
            dry_run=session.dry_run,
            interactive=session.interactive,
            current_stage=session.current_stage,
            next_stage=session.next_stage,
            completed_stages=session.completed_stages,
            state=state,
            session_path=session.session_path,
        )
        self._save_session(updated_session)
        if not request.resume:
            return updated_session
        return self.resume_run(run_id)

    def load_session(self, run_id: str) -> RunSession:
        payload = load_json(self._session_path(run_id))
        payload["state"] = DeliveryState.model_validate(payload["state"])
        return RunSession.model_validate(payload)

    def list_sessions(self) -> list[str]:
        return sorted(
            path.stem.replace("-session", "")
            for path in (self.settings.output_path / "runs").glob("*-session.json")
        )

    def _build_project_input(self, request: RunRequest, run_id: str):
        if request.input_path:
            return self.input_parser.read_input(Path(request.input_path))
        if request.raw_input:
            temp_path = self.settings.output_path / "runs" / f"{run_id}-input.md"
            temp_path.write_text(request.raw_input, encoding="utf-8")
            return self.input_parser.read_input(temp_path)
        raise ValueError("Either input_path or raw_input must be provided.")

    def _execute(
        self,
        *,
        run_id: str,
        state: DeliveryState,
        start_index: int,
        completed_stages: list[str],
        interactive: bool,
        stop_after_stage: str | None,
    ) -> RunSession:
        completed = list(completed_stages)
        for index in range(start_index, len(DEFAULT_FLOW)):
            stage = DEFAULT_FLOW[index]
            state = self.agents[stage].run(state)
            completed.append(stage)
            self._persist_artifacts(run_id, state)

            next_stage = DEFAULT_FLOW[index + 1] if index + 1 < len(DEFAULT_FLOW) else None
            should_pause = bool(next_stage) and (
                interactive or (stop_after_stage is not None and stage == stop_after_stage)
            )
            if should_pause:
                return self._save_session(
                    RunSession(
                        run_id=run_id,
                        status="waiting_for_intervention",
                        dry_run=bool(state.run_metadata.get("dry_run", False)),
                        interactive=interactive,
                        current_stage=stage,
                        next_stage=next_stage,
                        completed_stages=completed,
                        state=state,
                        session_path=str(self._session_path(run_id)),
                    )
                )

        return self._save_session(
            RunSession(
                run_id=run_id,
                status="completed",
                dry_run=bool(state.run_metadata.get("dry_run", False)),
                interactive=interactive,
                current_stage=DEFAULT_FLOW[-1],
                next_stage=None,
                completed_stages=completed,
                state=state,
                session_path=str(self._session_path(run_id)),
            )
        )

    def _persist_artifacts(self, run_id: str, state: DeliveryState) -> None:
        if state.project_blueprint is not None:
            self.repo_service.write_plan(run_id, state.project_blueprint.model_dump())
        self.repo_service.write_trace(
            run_id,
            [step.model_dump() for step in state.reasoning_trace],
        )
        if state.validation_report is not None:
            self.repo_service.write_report(
                run_id,
                {
                    "validation_report": state.validation_report.model_dump(),
                    "generated_files_index": (
                        state.generated_files_index.model_dump()
                        if state.generated_files_index is not None
                        else {}
                    ),
                    "c4_docs": state.c4_docs,
                },
            )

    def _patch_state(
        self,
        state: DeliveryState,
        state_field: str,
        patch: dict[str, Any],
    ) -> DeliveryState:
        if not hasattr(state, state_field):
            raise ValueError(f"Unsupported state field: {state_field}")

        current = getattr(state, state_field)
        if current is None:
            setattr(state, state_field, patch)
            return state

        if hasattr(current, "model_dump") and hasattr(type(current), "model_validate"):
            merged = current.model_dump()
            merged.update(patch)
            setattr(state, state_field, type(current).model_validate(merged))
            return state

        if isinstance(current, dict):
            merged = dict(current)
            merged.update(patch)
            setattr(state, state_field, merged)
            return state

        raise ValueError(f"State field {state_field} is not patchable.")

    def _save_session(self, session: RunSession) -> RunSession:
        dump_json(self._session_path(session.run_id), session.model_dump())
        return session

    def _session_path(self, run_id: str) -> Path:
        return self.settings.output_path / "runs" / f"{run_id}-session.json"
