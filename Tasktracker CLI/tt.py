import argparse
import json
from datetime import datetime
from typing import Optional
import os


class TaskTracker:

    def __init__(self) -> None:
        self.filename = "task.json"

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def get_time(self):
        return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # saves user input or changes
    @staticmethod
    def user_input_decorator(taskfunc):
        def wrapper(self, *args, **kwargs):
            result = taskfunc(self, *args, **kwargs)
            # tempfile for safety when saving file
            temp_file = self.filename + ".tmp"

            try:
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump({"tasks": self.tasks}, f,
                              indent=4, ensure_ascii=False)

                os.replace(temp_file, self.filename)  # safe replace

            except Exception as exc:
                print("Real ERROR:", repr(exc))
                raise

            return result

        return wrapper

    @user_input_decorator
    def add_task(self, task: str) -> int:
        if not task.strip():
            raise ValueError("please add a task.")

        task_data = {
            "id": max((t["id"] for t in self.tasks), default=0) + 1,
            "description": task,
            "status": "todo",
            "createdat": self.get_time(),
            "updatedat": self.get_time()
        }
        self.tasks.append(task_data)
        return task_data["id"]

    # lists all the tasks or status-filtered task
    def list_tasks(self, filter: Optional[str] = None) -> list:
        if filter is None:
            return self.tasks
        filtered_list = []
        for t in self.tasks:
            if t["status"] == filter:
                filtered_list.append(t)
        return filtered_list

    @user_input_decorator
    def update_tasks(self,
                     id: Optional[int] = None,
                     n_task: Optional[str] = None,
                     n_status: Optional[str] = None
                     ) -> None:

        if not self.tasks:
            print("No tasks available.")
            return

        # if no ID, shows tasks and ask user
        if id is None:
            print("Tasks:")
            for t in self.tasks:
                print(f"[{t['id']}] {t['description']} - {t['status']}")
            try:
                id = int(input("\nTask_ID: "))
            except ValueError:
                print("Invalid ID.")
                return

        for t in self.tasks:
            if t["id"] == id:

                if n_task is None:
                    n_task = input("update task: ").strip()
                if n_status is None:
                    n_status = input('update status: ').strip()

                if n_task:
                    t["description"] = n_task
                if n_status:
                    t["status"] = n_status

                t["updatedat"] = self.get_time()
                return

        raise IndexError(f"Task with ID {id} does not exist.")

    @user_input_decorator
    def delete_task(self, t_status: Optional[str] = None):
        if not self.tasks:
            print("No tasks available.")
            return
        # when status to delete isn't provided through CLI
        if t_status is None:
            print("Tasks:")
            for t in self.tasks:
                print(f"[{t['id']}] {t['description']} - {t['status']}")
            try:
                id = int(input("\nTask_ID: "))
            except ValueError:
                print("Invalid ID.")
                return

            for i, t in enumerate(self.tasks):
                if t["id"] == id:
                    self.tasks.pop(i)
                    return

            raise IndexError(f"Task with ID {id} does not exist.")
        # when status to delete is provided through CLI
        else:
            original_length = len(self.tasks)

            # remove all matching tasks safely
            self.tasks = [t for t in self.tasks if t["status"] != t_status]

            if len(self.tasks) == original_length:
                raise IndexError(f"No tasks with status '{t_status}' found.")


# The CLI component: Argparse
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

    # update task/status
    update_task_parser = subparsers.add_parser(
        "update", help="update a task or status")
    update_task_parser.add_argument(
        "id", type=int, nargs="?", help="finds the target task")
    update_task_parser.add_argument("--task", help="new task")
    update_task_parser.add_argument("--status", help="change in status")

    # delete task
    delete_task_parser = subparsers.add_parser(
        "delete", help="deletes selected task")
    delete_task_parser.add_argument(
        "status", type=str, nargs="?", help="deletes all task with that status")

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
        if args.command == "update":
            tracker.update_tasks(args.id, args.task, args.status)
            print(f"Task successfully updated at {tracker.get_time()}")
        if args.command == "delete":
            tracker.delete_task(args.status)
            print(f"Tasks with status '{args.status}' deleted.")

    except Exception as e:
        print(f"[error] {e}")


if __name__ == "__main__":
    main()
