from app.services import create_task, delete_task, list_tasks


def test_create_and_delete_task() -> None:
    initial = len(list_tasks())
    task = create_task(
        {
            "title": "Generated test task",
            "description": "Exercise generated backend service",
            "priority": "medium",
            "status": "todo",
            "due_date": "2026-04-02",
        }
    )
    assert len(list_tasks()) == initial + 1
    assert delete_task(task["id"]) is True
