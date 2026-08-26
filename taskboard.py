from dataclasses import dataclass


@dataclass
class Task:
    title: str
    completed: bool = False


class TaskBoard:
    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add(self, title: str) -> None:
        if not title.strip():
            raise ValueError("title must not be empty")
        self._tasks.append(Task(title=title))

    def complete(self, index: int) -> None:
        self._tasks[index].completed = True

    def open_titles(self) -> list[str]:
        return [task.title for task in self._tasks if not task.completed]

    def summary(self) -> dict[str, int | float]:
        total = len(self._tasks)
        completed = sum(task.completed for task in self._tasks)
        return {
            "total": total,
            "completed": completed,
            "open": total - completed,
            "completion_rate": completed / total if total else 0.0,
        }
