#!/usr/bin/env sh
set -eu

rm -rf workspace/generated_app/*
find outputs/runs -mindepth 1 -delete || true
find outputs/traces -mindepth 1 -delete || true
find outputs/plans -mindepth 1 -delete || true
find outputs/c4 -mindepth 1 -delete || true
touch outputs/runs/.gitkeep outputs/traces/.gitkeep outputs/plans/.gitkeep outputs/c4/.gitkeep
echo "Workspace nettoyé."
