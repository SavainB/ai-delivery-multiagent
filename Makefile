PYTHON ?= python3

.PHONY: install lint format test run dry-run serve export-traces clean bootstrap

install:
	uv sync --all-extras

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

run:
	uv run python -m ai_delivery.cli run --input inputs/sample_spec.md

dry-run:
	uv run python -m ai_delivery.cli run --input inputs/sample_spec.md --dry-run

serve:
	uv run python -m ai_delivery.cli serve --host 127.0.0.1 --port 8000

export-traces:
	uv run python scripts/export_traces.py

clean:
	sh scripts/clean_workspace.sh

bootstrap:
	sh scripts/bootstrap.sh
