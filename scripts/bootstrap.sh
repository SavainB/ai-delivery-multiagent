#!/usr/bin/env sh
set -eu

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed."
  echo "Install uv and rerun this script."
  exit 1
fi

uv sync --all-extras
uv run pre-commit install
echo "Environment ready."
