"""Input contracts."""

from __future__ import annotations

from typing import Any

from ai_delivery.utils.pydantic_compat import BaseModel, Field


class ProjectInput(BaseModel):
    source_path: str
    content: str
    content_type: str = "markdown"
    context: dict[str, Any] = Field(default_factory=dict)


class UserStory(BaseModel):
    title: str
    description: str
    acceptance_criteria: list[str] = Field(default_factory=list)


class ParsedRequirements(BaseModel):
    summary: str
    user_stories: list[UserStory] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    modules: list[str] = Field(default_factory=list)
    journeys: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
