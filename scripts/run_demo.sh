#!/usr/bin/env sh
set -eu

if ! command -v uv >/dev/null 2>&1; then
  echo "uv n'est pas installé."
  exit 1
fi

uv run python -m ai_delivery.cli run --input inputs/sample_spec.md
