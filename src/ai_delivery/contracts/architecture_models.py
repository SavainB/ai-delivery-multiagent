"""Architecture contracts."""

from __future__ import annotations

from ai_delivery.utils.pydantic_compat import BaseModel, Field


class C4Document(BaseModel):
    name: str
    description: str
    mermaid: str
    output_path: str


class ArchitectureDesign(BaseModel):
    overview: str
    backend_components: list[str] = Field(default_factory=list)
    frontend_components: list[str] = Field(default_factory=list)
    data_entities: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    c4_documents: list[C4Document] = Field(default_factory=list)
