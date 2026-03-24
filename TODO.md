# TODO.md

Living backlog for the `ai-delivery-multiagent` project.

Convention:

- `[x]` completed
- `[ ]` to do
- `P0` critical for a real project test
- `P1` important for a strong jury demo
- `P2` useful improvement but not blocking

## Estimated Overall Status

- overall progress: `~70%`
- very advanced on the generator skeleton, generator API, generator tests, and interactive demo flow
- the main gap is the real Snowflake provider and the depth of the generated application

## Already Done

- [x] Python monorepo structure for the generator
- [x] visible multi-agent orchestrator
- [x] FastAPI generator API
- [x] CLI with `run`, `resume`, `intervene`, `serve`
- [x] interactive mode with pauses between stages
- [x] typed central state
- [x] versioned prompts outside the codebase
- [x] generated C4 documentation
- [x] `uv`, `ruff`, `pytest`, `pre-commit`, CI tooling
- [x] generation of a target application in `workspace/generated_app/`
- [x] generator tests passing
- [x] complete linear repository walkthrough notebook (`REPOSITORY_WALKTHROUGH.ipynb`)

## P0 - Real Project Test

### 1. Connect the Real Snowflake Provider

- [ ] implement the real Snowflake call in [ai-delivery-multiagent/src/ai_delivery/llm/snowflake_provider.py](src/ai_delivery/llm/snowflake_provider.py)
- [ ] choose the exact integration mode:
  `AI_COMPLETE` SQL, Cortex Python, or REST
- [ ] add Snowflake config variables to [ai-delivery-multiagent/.env.example](.env.example)
- [ ] automatically load `.env` in [ai-delivery-multiagent/src/ai_delivery/settings.py](src/ai_delivery/settings.py)
- [ ] enrich [ai-delivery-multiagent/configs/models.yaml](configs/models.yaml) with the real Snowflake config
- [ ] convert Pydantic schemas into Snowflake-usable structured outputs
- [ ] handle network, auth, and parsing errors cleanly
- [ ] add unit tests for the mocked Snowflake provider
- [ ] add an integration test that can be enabled through environment variables

### 2. Make the Generated Application Truly Demoable

- [ ] replace in-memory storage with real SQLite in [ai-delivery-multiagent/src/ai_delivery/templates/backend/app/db.py](src/ai_delivery/templates/backend/app/db.py)
- [ ] connect backend CRUD to SQLite in [ai-delivery-multiagent/src/ai_delivery/templates/backend/app/services.py](src/ai_delivery/templates/backend/app/services.py)
- [ ] strengthen generated backend tests in [ai-delivery-multiagent/src/ai_delivery/templates/backend/tests/test_tasks.py](src/ai_delivery/templates/backend/tests/test_tasks.py)
- [ ] connect the generated frontend to the backend in [ai-delivery-multiagent/src/ai_delivery/templates/frontend/src/App.jsx](src/ai_delivery/templates/frontend/src/App.jsx)
- [ ] replace fake frontend local state with real API calls
- [ ] finalize real Tailwind configuration instead of only declaring the dependency
- [ ] regenerate [ai-delivery-multiagent/workspace/generated_app](workspace/generated_app) after upgrading the templates

## P1 - Strong Jury Demo

### 3. Strengthen the User Intervention Experience

- [ ] limit allowed interventions based on the current stage
- [ ] add simpler business endpoints:
  `approve`, `pause`, `cancel`
- [ ] make intervention errors more instructional
- [ ] document the interactive flow precisely in [ai-delivery-multiagent/README.md](README.md)
- [ ] add more interactive integration tests

### 4. Harden the Generated App Pipeline

- [ ] turn [ai-delivery-multiagent/.github/workflows/generated-app-ci.yml](.github/workflows/generated-app-ci.yml) into a real CI pipeline for the generated app
- [ ] truly verify the generated backend
- [ ] truly verify the generated frontend
- [ ] add a simple bootstrap procedure in the generated workspace
- [ ] add a fuller README in [ai-delivery-multiagent/workspace/generated_app/README.md](workspace/generated_app/README.md)

### 5. Improve the Demo

- [ ] enrich [ai-delivery-multiagent/inputs/sample_spec.md](inputs/sample_spec.md) with a more credible jury-ready spec
- [ ] improve [ai-delivery-multiagent/docs/demo-script.md](docs/demo-script.md) into a minute-by-minute script
- [ ] prepare a more realistic client branding example in [ai-delivery-multiagent/configs/clients/demo_brand.yaml](configs/clients/demo_brand.yaml)
- [ ] add a demo sequence in [ai-delivery-multiagent/scripts/run_demo.sh](scripts/run_demo.sh)

## P2 - Useful Improvements

### 6. Industrialization

- [ ] add authentication to the generator API
- [ ] replace simple JSON session persistence with more robust storage
- [ ] add more detailed observability
- [ ] remove `__pycache__` files from the repo and prevent them from coming back

### 7. Developer Experience

- [ ] add automatic `.env` loading
- [ ] add a `make demo` command
- [ ] add ready-to-copy `curl` examples to the README
- [ ] add dedicated FastAPI API tests with `TestClient`

## Recommended Order

1. `P0.1` real Snowflake provider
2. `P0.2` real SQLite and a stronger generated app
3. `P1.3` intervention experience
4. `P1.4` real generated app CI
5. `P1.5` demo polish

## Definition of Done Review

The project can be considered truly aligned with the original intent when:

- [ ] the real Snowflake provider is connected
- [ ] a full run works without mocks
- [ ] the user can intervene during generation through the API
- [ ] the generated app actually runs with backend + frontend
- [ ] the generated backend uses SQLite
- [ ] the generated frontend calls the backend API
- [ ] the generated app has useful CI
- [ ] the jury demo runs end to end

## Working Note

Current best practice:

- `AGENT.md` = stable project framing document
- `TODO.md` = living prioritized backlog
- `AGENTS.md` = usage guide for future Codex calls
