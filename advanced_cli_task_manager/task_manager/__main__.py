# advanced_cli_task_manager/task_manager/__main__.py

"""
Makes the task_manager package executable using `python -m task_manager`.
This simply imports and calls the main function from the cli module.
"""

from .cli import main  # Use relative import

if __name__ == "__main__":
    main()