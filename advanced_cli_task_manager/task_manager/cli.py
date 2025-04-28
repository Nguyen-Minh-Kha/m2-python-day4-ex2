# advanced_cli_task_manager/task_manager/cli.py

import argparse
from .core import add_task, list_tasks, delete_task # Relative imports
from .logger import logger # Relative import
from .config import TASKS_FILE # Relative import

def main():
    parser = argparse.ArgumentParser(
        description="A simple CLI Task Manager.",
        epilog="Example: python -m task_manager add 'Buy groceries' --priority high"
    )
    parser.add_argument(
        '--file',
        default=TASKS_FILE,
        help=f"Specify the path to the tasks JSON file (default: {TASKS_FILE})"
    )
    # Make subparsers mandatory
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # --- Add Task Subcommand ---
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="The description of the task")
    parser_add.add_argument(
        "-p", "--priority", type=str, default="normal",
        choices=["low", "normal", "high"], help="The priority of the task (low, normal, high)"
    )

    # --- List Tasks Subcommand ---
    parser_list = subparsers.add_parser("list", help="List all tasks")
    # No specific arguments needed for list

    # --- Delete Task Subcommand ---
    parser_delete = subparsers.add_parser("delete", help="Delete a task by its ID")
    parser_delete.add_argument("task_id", type=int, help="The ID of the task to delete")

    # --- Parse Arguments ---
    args = parser.parse_args()

    # Use the specified task file from arguments
    tasks_file_path = args.file

    # --- Execute Commands ---
    if args.command == "add":
        logger.info(f"CLI: Received 'add' command. Desc='{args.description}', Prio='{args.priority}'")
        new_task = add_task(args.description, args.priority, tasks_file=tasks_file_path)
        if new_task:
            print(f"✅ Task added with ID: {new_task['id']}")
        else:
            print("❌ Failed to add task.") # Core function already prints specific error

    elif args.command == "list":
        logger.info("CLI: Received 'list' command.")
        tasks = list_tasks(tasks_file=tasks_file_path)
        if not tasks:
            print("No tasks found.")
        else:
            print("\n--- Task List ---")
            # Sort tasks by ID for consistent display
            tasks.sort(key=lambda x: x.get('id', 0))
            for task in tasks:
                print(f"  ID: {task.get('id', 'N/A')}, Desc: {task.get('description', 'N/A')}, "
                      f"Prio: {task.get('priority', 'N/A')}, Status: {task.get('status', 'N/A')}")
            print("-----------------\n")

    elif args.command == "delete":
        logger.info(f"CLI: Received 'delete' command. ID={args.task_id}")
        deleted = delete_task(args.task_id, tasks_file=tasks_file_path)
        if deleted:
            print(f"✅ Task with ID {args.task_id} deleted successfully.")
        else:
            print(f"❌ Task with ID {args.task_id} not found.")

    else:
        # This part should not be reached if subparsers are required=True
        logger.warning("CLI: No command provided.")
        parser.print_help()

# This allows running the CLI using "python -m task_manager ..."
if __name__ == "__main__":
    main()
