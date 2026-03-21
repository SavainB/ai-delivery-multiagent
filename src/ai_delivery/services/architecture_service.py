"""Architecture generation service."""

from __future__ import annotations

from ai_delivery.contracts import (
    ArchitectureDesign,
    C4Document,
    ParsedRequirements,
    ProjectBlueprint,
)
from ai_delivery.llm.structured_output import generate_with_schema
from ai_delivery.tools.diagram_tools import (
    build_component_diagram,
    build_container_diagram,
    build_context_diagram,
)
from ai_delivery.tools.filesystem import write_text


class ArchitectureService:
    def __init__(self, provider, prompt_loader, settings) -> None:  # noqa: ANN001
        self.provider = provider
        self.prompt_loader = prompt_loader
        self.settings = settings

    def design(
        self,
        requirements: ParsedRequirements,
        blueprint: ProjectBlueprint,
    ) -> ArchitectureDesign:
        prompt = self.prompt_loader.load_bundle(
            "shared/system_common.txt",
            "agents/architect.txt",
            "tasks/design_architecture.txt",
        )
        design = generate_with_schema(
            self.provider,
            prompt,
            ArchitectureDesign,
            {
                "requirements": requirements.model_dump(),
                "blueprint": blueprint.model_dump(),
            },
        )
        design.c4_documents = [
            C4Document(
                name="context",
                description="Context view of the generator and the target application.",
                mermaid=build_context_diagram(blueprint.project_name),
                output_path="docs/c4-context.md",
            ),
            C4Document(
                name="container",
                description="Container view of the generator.",
                mermaid=build_container_diagram(),
                output_path="docs/c4-container.md",
            ),
            C4Document(
                name="component",
                description="Component view of the generation chain.",
                mermaid=build_component_diagram(),
                output_path="docs/c4-component.md",
            ),
        ]
        return design

    def persist_c4_docs(self, design: ArchitectureDesign) -> list[dict[str, str]]:
        persisted: list[dict[str, str]] = []
        for doc in design.c4_documents:
            doc_path = self.settings.root_dir / doc.output_path
            content = "\n".join(
                [
                    f"# C4 {doc.name.title()}",
                    "",
                    doc.description,
                    "",
                    "```mermaid",
                    doc.mermaid,
                    "```",
                    "",
                ]
            )
            write_text(doc_path, content)
            output_path = self.settings.output_path / "c4" / f"{doc.name}.md"
            write_text(output_path, content)
            persisted.append(
                {
                    "name": doc.name,
                    "doc_path": str(doc_path),
                    "output_path": str(output_path),
                }
            )
        return persisted
