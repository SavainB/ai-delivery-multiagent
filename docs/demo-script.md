# Demo Script

## Preparation

1. Activate the virtual environment.
2. Start the generator API:
   `python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000`

## Live Demo

1. Show `IBM.docx` and restate the hackathon topic.
2. Explain the separation between:
   - the generator API
   - the generated application in `workspace/generated_app/`
3. Verify the API:
   `curl http://127.0.0.1:8000/health`
4. Start an interactive run:
   `POST /runs`
5. Show the pause after `spec_analyst`.
6. Inspect the run state with `GET /runs/{run_id}`.
7. Resume the run until the next pause.
8. Show the artifacts already written:
   - `outputs/plans/`
   - `outputs/traces/`
   - `outputs/c4/`
9. Continue until the end.
10. Open `workspace/generated_app/`.
11. Show the generated backend/frontend structure.
12. Show the CI, tests, and branding hooks.

## Message to Make Explicit to the Jury

- the system is already demoable end to end
- the mock provider enables the local demo
- the next milestone is the real Snowflake connection
