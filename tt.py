import argparse
import json
from datetime import datetime


class TaskTracker:
    # Handles the task tracking.

    def __init__(self) -> None:
        self.filename = "task.json"
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    @staticmethod
    def user_input_decorator(taskfunc):
        def wrapper(self, *args, **kwargs):
            result = taskfunc(self, *args, **kwargs)
            try:
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump({"tasks": self.tasks}, f,
                              indent=4, ensure_ascii=False)
            except Exception as exc:
                raise IOError("could not write data to file.") from exc

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

    def list_tasks(self, filter: str = None) -> list:
        if filter is None:
            return self.tasks
        filtered_list = []
        for t in self.tasks:
            if t["status"] == filter:
                filtered_list.append(t)


def main():
    parser = argparse.ArgumentParser(description="Tasktracker CLI")

    subparsers = parser.add_subparsers(dest="command")

    # add tasks
    add_task_parser = subparsers.add_parser("add", help="adds new task")
    add_task_parser.add_argument("text", help="task to save")

    # list tasks
    list_task_parser = subparsers.add_parser("list", help="lists all tasks")
    list_task_parser.add_argument(
        "stat",
        type=str,
        nargs="?",
        help="group according to it's status"
    )

    args = parser.parse_args()

    tracker = TaskTracker()

    try:
        if args.command == "add":
            tracker.add_task(args.text)
            print(f"Task successfully added, (ID: {len(tracker.tasks)})")
        if args.command == "list":
            tasks = tracker.list_tasks(args.stat)
            if not tasks:
                print(
                    f"No tasks found{' with status: ' + args.stat if args.stat else ''}"
                )
            else:
                print(
                    f"Tasks{' with status: ' + args.stat if args.stat else ''}:")
                for task in tasks:
                    print(
                        f"[{task['id']}] {task['description']} - {task['status']}")
    except Exception as e:
        print(f"[error] {e}")


if __name__ == "__main__":
    main()
