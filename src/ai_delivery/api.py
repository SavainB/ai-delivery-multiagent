"""FastAPI entrypoint for the multi-agent generator."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from ai_delivery.contracts.session_models import InterventionRequest, RunRequest, RunSession
from ai_delivery.services.session_service import SessionService
from ai_delivery.settings import load_settings

app = FastAPI(title="AI Delivery Multi-Agent API", version="0.1.0")


def _session_service() -> SessionService:
    return SessionService(load_settings())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/runs")
def list_runs() -> dict[str, list[str]]:
    return {"runs": _session_service().list_sessions()}


@app.post("/runs", response_model=RunSession)
def create_run(request: RunRequest) -> RunSession:
    try:
        return _session_service().start_run(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/runs/{run_id}", response_model=RunSession)
def get_run(run_id: str) -> RunSession:
    try:
        return _session_service().load_session(run_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown run_id: {run_id}") from exc


@app.post("/runs/{run_id}/resume", response_model=RunSession)
def resume_run(run_id: str) -> RunSession:
    try:
        return _session_service().resume_run(run_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown run_id: {run_id}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/runs/{run_id}/interventions", response_model=RunSession)
def intervene(run_id: str, request: InterventionRequest) -> RunSession:
    try:
        return _session_service().apply_intervention(run_id, request)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown run_id: {run_id}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
