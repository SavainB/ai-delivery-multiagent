# Architecture

The repository explicitly separates:

- the Python multi-agent generator
- the generated demo application in `workspace/generated_app/`

## Overview

The system has two distinct surfaces:

1. a **generator API** that drives runs
2. a **generated application** written in `workspace/generated_app/`

The generator API is therefore not the final business application. It orchestrates the software delivery pipeline.

## Agent Flow

The pipeline is orchestrated through a simple flow:

1. `spec_analyst`
2. `architect`
3. `developer`
4. `qa_devops`
5. `reviewer`

Each stage reads and enriches a typed central state.

Intermediate artifacts are persisted in `outputs/`.

## Interactive API

The generator exposes:

- `POST /runs`
- `GET /runs/{run_id}`
- `POST /runs/{run_id}/resume`
- `POST /runs/{run_id}/interventions`

When interactive mode is enabled, the pipeline pauses between stages so the user can:

- review the system's understanding of the requirement
- correct a summary or plan
- adjust some decisions before the next stage

## Central State

The shared state contains at least:

- `raw_input`
- `parsed_requirements`
- `project_blueprint`
- `architecture_design`
- `generated_files_index`
- `c4_docs`
- `validation_report`
- `reasoning_trace`
- `run_metadata`
- `errors`

## LLM Provider

The architecture includes an abstract provider layer.

Current status:

- `mock`: operational
- `snowflake`: structure present, real integration still to be connected

## Generated Application

The generated workspace currently contains:

- a lightweight FastAPI backend
- a lightweight React/Vite frontend
- base files for the demo

This workspace still needs to be strengthened to reach the final target:

- real SQLite
- real frontend/backend integration
- more substantial CI
