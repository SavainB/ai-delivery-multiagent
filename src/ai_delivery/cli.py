"""Command line interface."""

from __future__ import annotations

import argparse
import json

import uvicorn

from ai_delivery.contracts.session_models import InterventionRequest, RunRequest
from ai_delivery.logging_config import configure_logging
from ai_delivery.main import run_pipeline
from ai_delivery.services.session_service import SessionService
from ai_delivery.settings import load_settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-delivery")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full pipeline")
    run_parser.add_argument("--input", required=True)
    run_parser.add_argument("--settings")
    run_parser.add_argument("--dry-run", action="store_true")
    run_parser.add_argument("--interactive", action="store_true")

    resume_parser = subparsers.add_parser("resume", help="Resume an interactive run")
    resume_parser.add_argument("--run-id", required=True)
    resume_parser.add_argument("--settings")

    intervene_parser = subparsers.add_parser(
        "intervene",
        help="Patch state and optionally resume an interactive run",
    )
    intervene_parser.add_argument("--run-id", required=True)
    intervene_parser.add_argument("--state-field", required=True)
    intervene_parser.add_argument("--patch-json", default="{}")
    intervene_parser.add_argument("--no-resume", action="store_true")
    intervene_parser.add_argument("--settings")

    serve_parser = subparsers.add_parser("serve", help="Serve the generator API")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)

    docs_parser = subparsers.add_parser("generate-docs", help="Generate documentation only")
    docs_parser.add_argument("--input", required=True)
    docs_parser.add_argument("--settings")

    scaffold_parser = subparsers.add_parser("generate-app", help="Generate application scaffold")
    scaffold_parser.add_argument("--input", required=True)
    scaffold_parser.add_argument("--settings")

    subparsers.add_parser("export-traces", help="List available traces")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        service = SessionService(load_settings(args.settings))
        session = service.start_run(
            RunRequest(
                input_path=args.input,
                dry_run=args.dry_run,
                interactive=args.interactive,
            )
        )
        print(json.dumps(session.model_dump(), indent=2, ensure_ascii=True))
        return 0

    if args.command == "resume":
        session = SessionService(load_settings(args.settings)).resume_run(args.run_id)
        print(json.dumps(session.model_dump(), indent=2, ensure_ascii=True))
        return 0

    if args.command == "intervene":
        patch = json.loads(args.patch_json)
        session = SessionService(load_settings(args.settings)).apply_intervention(
            args.run_id,
            InterventionRequest(
                state_field=args.state_field,
                patch=patch,
                resume=not args.no_resume,
            ),
        )
        print(json.dumps(session.model_dump(), indent=2, ensure_ascii=True))
        return 0

    if args.command == "serve":
        uvicorn.run("ai_delivery.api:app", host=args.host, port=args.port, reload=False)
        return 0

    if args.command == "generate-docs":
        run_pipeline(input_path=args.input, dry_run=True, settings_path=args.settings)
        return 0

    if args.command == "generate-app":
        run_pipeline(input_path=args.input, dry_run=False, settings_path=args.settings)
        return 0

    if args.command == "export-traces":
        settings = load_settings()
        traces = sorted((settings.output_path / "traces").glob("*.json"))
        print("\n".join(str(path) for path in traces))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
