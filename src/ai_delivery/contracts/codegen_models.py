"""Code generation contracts."""

from __future__ import annotations

from ai_delivery.utils.pydantic_compat import BaseModel, Field


class FileArtifact(BaseModel):
    path: str
    category: str
    description: str


class GeneratedAppManifest(BaseModel):
    app_name: str
    backend_files: list[FileArtifact] = Field(default_factory=list)
    frontend_files: list[FileArtifact] = Field(default_factory=list)
    support_files: list[FileArtifact] = Field(default_factory=list)
