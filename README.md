# AI Delivery Multi-Agent

Hackathon repository for a Python multi-agent system that turns a requirement expression into the main artifacts of a software delivery pipeline.

## Goal

This repository contains the **generator**.
The demo task-management application is produced in `workspace/generated_app/`.

## Current Status

The project is currently in a **demoable** state, but it is not yet fully finished for a real Snowflake-backed run.

What already works:

- visible multi-agent orchestrator
- FastAPI generator API
- interactive stage-by-stage execution
- generation of plans, traces, and C4 documentation
- generation of a target application in `workspace/generated_app/`
- quality tooling for the main repository

What still needs to be finalized:

- real Snowflake provider integration
- real SQLite persistence in the generated app
- real frontend-to-backend wiring in the generated app
- more substantial CI for the generated application

## Capabilities

- analysis of a text, Markdown, or JSON specification
- structured planning and project blueprint generation
- Mermaid C4 documentation
- generation of a FastAPI + React/Vite/Tailwind application
- generation of CI/CD and validation scripts
- export of `Plan / Act / Reason` traces
- `dry-run` execution mode
- generator exposed as an API
- user intervention between key stages

## Stack

- Python 3.11
- LangGraph with a local sequential fallback
- Pydantic through a compatibility layer
- uv for dependency management
- Ruff for lint + format
- pytest for tests
- GitHub Actions for CI

## Getting Started

With the existing environment:

```bash
source .venv/bin/activate
python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000
```

With `uv`:

```bash
uv sync --all-extras
uv run pre-commit install
uv run python -m ai_delivery.cli run --input inputs/sample_spec.md
```

Demo mode without real generation:

```bash
uv run python -m ai_delivery.cli run --input inputs/sample_spec.md --dry-run
```

Local API:

```bash
uv run python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000
```

## Snowflake Preparation

The repository is prepared for a future real Snowflake provider, but that provider is not yet wired end to end.

Expected setup:

1. copy the example file:

```bash
cp .env.example .env
```

2. fill the Snowflake variables in `.env` or in your shell:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`
- `SNOWFLAKE_HOST`
- `SNOWFLAKE_AUTHENTICATOR`
- `SNOWFLAKE_CORTEX_MODEL`

3. switch the provider:

```bash
export AI_DELIVERY_PROVIDER=snowflake
```

4. implement the real connection in `src/ai_delivery/llm/snowflake_provider.py`

Current status:

- the Snowflake configuration surface is prepared
- the `snowflake` provider exists as an extension point
- the real runtime behavior still has to be implemented

## What You Are Actually Driving

The API exposed on `127.0.0.1:8000` drives the **generator**.

You are not directly driving the final ToDo application.

The real flow is:

1. you start a run
2. the system executes an agent
3. it persists the current state
4. it pauses if interactive mode is enabled
5. you inspect or modify the state
6. you resume the run
7. the final artifacts are written to `outputs/` and `workspace/generated_app/`

## Useful Commands

```bash
make install
make lint
make format
make test
make run
make dry-run
make serve
make export-traces
make clean
```

## API and User Intervention

The generator exposes a FastAPI API:

- `POST /runs` to start a run
- `GET /runs/{run_id}` to inspect a state
- `POST /runs/{run_id}/resume` to resume an interactive run
- `POST /runs/{run_id}/interventions` to modify the state before resuming

In `interactive` mode, the pipeline pauses after each agent. The user can intervene on:

- `parsed_requirements`
- `project_blueprint`
- `architecture_design`
- `run_metadata`

Example of a minimal cycle:

```bash
curl -X POST http://127.0.0.1:8000/runs \
  -H 'content-type: application/json' \
  -d '{"input_path":"inputs/sample_spec.md","interactive":true,"dry_run":true}'

curl http://127.0.0.1:8000/runs/<RUN_ID>

curl -X POST http://127.0.0.1:8000/runs/<RUN_ID>/resume
```

## Structure

- `src/ai_delivery/` : orchestrator, services, agents, and tools
- `prompts/` : versioned prompts outside Python code
- `configs/` : global configuration, model settings, demo branding
- `inputs/` : input examples
- `outputs/` : plans, traces, C4 exports, and reports
- `workspace/generated_app/` : generated application
- `docs/` : architecture documentation and ADRs

## Demo

The nominal pipeline is:

1. read the requirement
2. produce the structured analysis
3. optional user pause after `spec_analyst`
4. define the architecture
5. optional user pause after `architect`
6. generate application artifacts
7. optional user pause after `developer`
8. perform quality / CI validation
9. produce the final review

See `docs/demo-script.md` for the demo narrative.

## Quick Manual Test

```bash
curl -X POST http://127.0.0.1:8000/runs \
  -H 'content-type: application/json' \
  -d '{"input_path":"inputs/sample_spec.md","interactive":true,"dry_run":true}'
```

Then:

1. get the `run_id`
2. inspect `GET /runs/{run_id}`
3. intervene if needed with `POST /runs/{run_id}/interventions`
4. resume with `POST /runs/{run_id}/resume`

## Artifacts to Inspect

- `outputs/plans/` : project blueprint
- `outputs/traces/` : `Plan / Act / Reason` traces
- `outputs/c4/` : C4 exports
- `outputs/runs/` : sessions and reports
- `workspace/generated_app/` : generated application

## Known Limitations

- the real Snowflake provider is not connected yet
- the current `snowflake` provider still falls back to mock behavior
- the generated application is demoable but not yet fully aligned with the target:
  the backend is still light, the frontend is not yet truly connected to the backend, and SQLite is not finished

## Configuration Sources

Today, the project configuration relies mainly on:

- `pyproject.toml`
- `configs/settings.yaml`
- `configs/models.yaml`
- shell environment variables

The `.env.example` file is ready for Snowflake, but automatic `.env` loading is still a remaining task.
