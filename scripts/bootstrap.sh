#!/usr/bin/env sh
set -eu

if ! command -v uv >/dev/null 2>&1; then
  echo "uv n'est pas installé."
  echo "Installe uv puis relance ce script."
  exit 1
fi

uv sync --all-extras
uv run pre-commit install
echo "Environnement prêt."
