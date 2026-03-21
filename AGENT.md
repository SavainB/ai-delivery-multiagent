# AGENT.md

## Repository Goal

Build a **Python multi-agent system** that takes a requirement expression as input and autonomously produces the main artifacts of a software delivery pipeline.

The main repository is **the generator**.
The demo application produced by this generator must be written to `workspace/generated_app/`.

The source brief is `IBM.docx` at the repository root.

## Source of Truth

The project must reconcile two sources:

1. The IBM brief contained in `IBM.docx`
2. The architecture choice already validated by the user

If several design options compete:

- prefer simplicity
- prefer determinism
- prefer demo reliability
- avoid excessive agent autonomy

## Faithful Summary of the IBM Brief

### Overall Functional Goal

The system must take a requirement expression as input, for example:

- functional specifications
- free text
- sketches
- visual material
- mockups

Then it must produce the main artifacts of a software pipeline:

- requirement analysis
- project plan
- architecture documentation
- repository structure
- application code
- tests
- CI/CD
- reasoning traces

### Expected Capabilities

The system must be able to:

- analyze input specifications
- identify modules, user journeys, constraints, and components
- create a development environment
- initialize a Git repository
- generate the project scaffold
- configure a CI/CD pipeline
- produce architecture documentation based on the C4 model
- generate application code
- generate unit tests
- generate an interface adaptable to the client context
- expose `Plan / Act / Reason` reasoning traces

### IBM Technical Constraints

- use **at least one open-source LLM**
- use an **open-source agent framework**
- justify the agent framework choice
- produce a solution that is defensible in an enterprise context

### IBM Demo Candidate Application

The expected demo application is a **simple task management application** in a ToDo / request-tracking style with:

- simplified user identification or login
- a filterable dashboard
- task creation / update / deletion
- a detail page with description, priority, due date, and status
- optionally: assignment, comments, history

## Approved Architecture Decisions

These choices are considered validated and should not be reopened without strong reason:

- main language: `Python 3.11`
- project management: `uv`
- lint and format: `ruff`
- Git hooks: `pre-commit`
- tests: `pytest`
- multi-agent orchestration: `LangGraph`
- prompt/tool/parsing support: `LangChain` only if useful, not as the dominant layer
- typed contracts: `Pydantic`
- abstract LLM provider: generic interface + Snowflake-oriented implementation
- generated backend: `FastAPI`
- generated frontend: `React + Vite + Tailwind`
- demo database: `SQLite`
- CI/CD: `GitHub Actions`
- C4 documentation: `Mermaid`

## Guiding Repository Principle

The main repository is **not** the ToDo application itself.

The main repository contains:

- the multi-agent orchestrator
- prompts
- data models
- generation tools
- templates
- demo scripts
- outputs and traces

The generated application must live under:

- `workspace/generated_app/`

## Target Repository Structure

The reference target structure is:

```text
ai-delivery-multiagent/
├─ .github/workflows/
├─ prompts/
├─ configs/
├─ inputs/
├─ outputs/
├─ workspace/generated_app/
├─ src/ai_delivery/
├─ tests/
├─ docs/
└─ scripts/
```

## Agents to Implement

### `spec_analyst`

- analyze user inputs
- identify user stories, modules, constraints, journeys, and components
- produce an initial usable structure
- produce a validated JSON output

### `architect`

- define the overall architecture
- propose the backend/frontend split
- define the data model
- prepare the generated project structure
- produce the C4 artifacts

### `developer`

- generate the backend in `workspace/generated_app/`
- generate the frontend in `workspace/generated_app/`
- generate the first tests
- generate the produced application README

### `qa_devops`

- generate CI/CD
- add local validation
- verify lint and tests
- propose or apply simple fixes

### `reviewer`

- verify consistency across requirement, architecture, code, and traces
- produce a final report usable in the demo

## Recommended Workflow

Nominal flow:

```text
START
-> spec_analyst
-> architect
-> developer
-> qa_devops
-> reviewer
-> END
```

The graph must remain **simple, readable, and deterministic**.

## Central State to Provide

The `src/ai_delivery/state.py` file must define a typed central state containing at least:

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

## LLM Provider Layer

Expected files:

- `src/ai_delivery/llm/base.py`
- `src/ai_delivery/llm/snowflake_provider.py`
- `src/ai_delivery/llm/structured_output.py`
- `src/ai_delivery/llm/prompt_loader.py`

Rules:

- no strong dependency from the rest of the system on a concrete provider
- allow a future real Snowflake provider
- keep a mock/fake path for local demo use
- validate structured outputs with Pydantic
- handle parsing errors cleanly
- keep retries bounded and traceable

## Prompt Management

Prompts must be **stored in files**, never as large inline blocks in Python code.

## Expected Generated Application

The system must generate a task management application in `workspace/generated_app/`.

### Generated Backend

- `FastAPI`
- `SQLite`
- task CRUD API
- separated routers / services / models

### Generated Frontend

- `React`
- `Vite`
- `Tailwind`
- dashboard
- filterable task list
- task detail
- create / edit form
- configurable branding

## C4 Documentation

The system must produce at least:

- context diagram
- container diagram
- component diagram
- short technical description

Recommended format:

- `Mermaid` embedded in `.md` files

## Definition of Done

The project must not be considered finished until the following are true:

- the pipeline can be launched through CLI and API
- traces are written to `outputs/traces/`
- a plan is written to `outputs/plans/`
- the generated app exists in `workspace/generated_app/`
- the generated backend exposes task CRUD
- the generated frontend lets users manipulate tasks
- `pre-commit` is configured
- the real Snowflake provider is connected for a non-mock test

## Anti-Patterns to Avoid

- notebook-based architecture
- a single monolithic script
- prompts hidden in code
- agents with fuzzy responsibilities
- mandatory dependence on an external LLM service for the local demo
- purely cosmetic frontend with no API integration

## Working Convention

For future Codex calls:

1. read `AGENT.md`
2. treat this file as the project framing contract
3. check `IBM.docx` only if doubt remains about the brief
4. implement without reopening decisions already made here unless a major contradiction appears
