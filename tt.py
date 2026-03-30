import argparse
import json
from datetime import datetime


class TaskTracker:
    # Handles the task tracking.

    def __init__(self) -> None:
        self.filename = "task.json"
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    @staticmethod
    def user_input_decorator(taskfunc):
        def wrapper(self, *args, **kwargs):
            result = taskfunc(self, *args, **kwargs)
            try:
                with open(self.filename, "w") as f:
                    json.dump({"tasks": self.tasks}, f, indent=4)
            except Exception:
                raise IOError("could not write data to file.")

            return result

        return wrapper

    @user_input_decorator
    def add_task(self, task: str) -> int:
        if not task.strip():
            raise ValueError("please add a task.")
        time = datetime.now()
        currentTime = time.strftime("%m/%d/%Y, %H:%M:%S")
        task_data = {
            "id": max((t["id"] for t in self.tasks), default=0) + 1,
            "description": task,
            "status": "todo",
            "createdat": currentTime,
            "updatedat": currentTime
        }
        self.tasks.append(task_data)
        return task_data["id"]


def main():
    parser = argparse.ArgumentParser(description="Tasktracker CLI")
    parser.add_argument("task", help="add task")

    args = parser.parse_args()

    tracker = TaskTracker()
    tracker.add_task(args.task)


if __name__ == "__main__":
    main()
