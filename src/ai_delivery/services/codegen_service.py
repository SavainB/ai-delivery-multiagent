"""Generated application scaffolding service."""

from __future__ import annotations

from pathlib import Path

from ai_delivery.contracts import FileArtifact, GeneratedAppManifest
from ai_delivery.tools.filesystem import (
    ensure_directory,
    list_files,
    render_template,
    write_text,
)


class CodegenService:
    def __init__(self, settings, branding_service) -> None:  # noqa: ANN001
        self.settings = settings
        self.branding_service = branding_service

    def generate_app(self, dry_run: bool = False) -> GeneratedAppManifest:
        workspace = self.settings.workspace_path
        ensure_directory(workspace)
        if dry_run:
            return GeneratedAppManifest(app_name="Dry Run App")

        context = self._template_context()
        backend_root = self.settings.templates_path / "backend"
        frontend_root = self.settings.templates_path / "frontend"

        self._render_tree(backend_root, workspace / "backend", context)
        self._render_tree(frontend_root, workspace / "frontend", context)
        self._write_support_files(workspace, context)

        return GeneratedAppManifest(
            app_name=context["APP_NAME"],
            backend_files=self._artifact_list(workspace / "backend", "backend"),
            frontend_files=self._artifact_list(workspace / "frontend", "frontend"),
            support_files=self._artifact_list(
                workspace, "support", exclude={"backend", "frontend"}
            ),
        )

    def _template_context(self) -> dict[str, str]:
        brand = self.branding_service.load()
        return {
            "APP_NAME": brand.get("application_name", "Generated Task App"),
            "CLIENT_NAME": brand.get("client_name", "Demo Client"),
            "PRIMARY_COLOR": brand.get("primary_color", "#0d3b66"),
            "SECONDARY_COLOR": brand.get("secondary_color", "#f4d35e"),
            "ACCENT_COLOR": brand.get("accent_color", "#ee964b"),
            "SURFACE_COLOR": brand.get("surface_color", "#faf0ca"),
            "LOGO_TEXT": brand.get("logo_text", "DeliveryFlow"),
            "FONT_FAMILY": brand.get("font_family", '"Space Grotesk", sans-serif'),
        }

    def _render_tree(
        self,
        source_root: Path,
        target_root: Path,
        context: dict[str, str],
    ) -> None:
        for path in source_root.rglob("*"):
            if path.is_dir():
                continue
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            relative = path.relative_to(source_root)
            target = target_root / relative
            content = path.read_text(encoding="utf-8")
            write_text(target, render_template(content, context))

    def _write_support_files(self, workspace: Path, context: dict[str, str]) -> None:
        readme = "\n".join(
            [
                f"# {context['APP_NAME']}",
                "",
                f"Application de demonstration generee pour {context['CLIENT_NAME']}.",
                "",
                "## Structure",
                "",
                "- `backend/` : API FastAPI",
                "- `frontend/` : interface React",
            ]
        )
        write_text(workspace / "README.md", readme + "\n")

    def _artifact_list(
        self, root: Path, category: str, exclude: set[str] | None = None
    ) -> list[FileArtifact]:
        exclude = exclude or set()
        artifacts: list[FileArtifact] = []
        for path in list_files(root):
            relative = path.relative_to(self.settings.workspace_path)
            if relative.parts and relative.parts[0] in exclude:
                continue
            artifacts.append(
                FileArtifact(
                    path=str(relative),
                    category=category,
                    description=f"Generated {category} artifact",
                )
            )
        return artifacts
