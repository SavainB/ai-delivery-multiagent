"""Convenience wrapper for C4 generation."""

from __future__ import annotations


class C4Service:
    def __init__(self, architecture_service) -> None:  # noqa: ANN001
        self.architecture_service = architecture_service

    def generate(self, design):  # noqa: ANN001
        return self.architecture_service.persist_c4_docs(design)
