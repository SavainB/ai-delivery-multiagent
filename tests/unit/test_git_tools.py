from ai_delivery.tools.git_tools import is_git_repo
from ai_delivery.utils.paths import project_root


def test_is_git_repo_true_for_project_root() -> None:
    assert is_git_repo(project_root()) is True
