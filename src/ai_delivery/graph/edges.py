"""Directed edges for the deterministic workflow."""

from __future__ import annotations

from ai_delivery.graph import nodes

DEFAULT_FLOW = [
    nodes.SPEC_ANALYST,
    nodes.ARCHITECT,
    nodes.DEVELOPER,
    nodes.QA_DEVOPS,
    nodes.REVIEWER,
]
