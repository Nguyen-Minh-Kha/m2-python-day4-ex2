# Advanced CLI Task Manager

A simple command-line interface (CLI) tool to manage tasks, built with Python.

## Features

*   Add tasks with descriptions and priorities.
*   List all pending tasks.
*   Delete tasks by their ID.
*   Tasks are stored in a JSON file (`tasks.json` by default).
*   Actions are logged to `logs/task_manager.log`.
*   Task file location can be configured via the `TASKS_FILE_PATH` environment variable or the `--file` command-line argument.

## Folder Structure

```plaintext
advanced_cli_task_manager/
│── task_manager/          # CLI Tool Source Code
│   │── __init__.py
│   │── cli.py             # CLI Entry Point
│   │── core.py            # Core Logic
│   │── logger.py          # Logging Setup
│   │── config.py          # Configuration Management
│── tests/                 # Unit Tests
│   │── __init__.py
│   │── test_core.py
│   │── test_tasks.json    # Temporary file created during tests
│── tasks.json             # JSON File for Storing Tasks
│── logs/                  # Log files directory
│   │── task_manager.log
│── requirements.txt       # Dependencies (currently none)
│── README.md              # This file
```

## Examples

```shell
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Add a high-priority task
python -m task_manager add "Finish project report" --priority high

# Add a normal-priority task
python -m task_manager add "Buy milk"

# List all tasks
python -m task_manager list

# Delete task with ID 1
python -m task_manager delete 1

# Use a custom task file
export TASKS_FILE_PATH="/path/to/my/special_tasks.json"
python -m task_manager list

# Or specify file via command line
python -m task_manager list --file "/path/to/another/tasks.json"
```

## Unittest

```shell
python -m unittest discover tests
# or
python tests/test_core.py
```
