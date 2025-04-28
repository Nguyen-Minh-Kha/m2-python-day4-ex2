# advanced_cli_task_manager/task_manager/config.py

import os

# Get the tasks file path from environment variable or use default
# Default is 'tasks.json' in the parent directory of 'task_manager' package
DEFAULT_TASKS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.json")
TASKS_FILE = os.getenv("TASKS_FILE_PATH", DEFAULT_TASKS_FILE)

# You could add other configurations here later if needed
# e.g., DEFAULT_PRIORITY = "normal"
