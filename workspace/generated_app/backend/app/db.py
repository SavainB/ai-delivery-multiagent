from collections.abc import Iterable

TASKS: list[dict] = [
    {
        "id": 1,
        "title": "Kickoff demo",
        "description": "Prepare the first generated delivery demo.",
        "priority": "high",
        "status": "todo",
        "due_date": "2026-04-01",
    }
]


def all_tasks() -> Iterable[dict]:
    return TASKS
