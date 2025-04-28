# advanced_cli_task_manager/task_manager/core.py

import json
import os
from .logger import logger # Use relative import within the package
from .config import TASKS_FILE # Use relative import

def load_tasks(tasks_file=TASKS_FILE):
    """Loads tasks from the JSON file."""
    try:
        if not os.path.exists(tasks_file):
            logger.info(f"Task file '{tasks_file}' not found. Starting with empty list.")
            return [] # Return empty list if file doesn't exist
        with open(tasks_file, 'r') as f:
            tasks = json.load(f)
            logger.debug(f"Tasks loaded successfully from {tasks_file}.")
            return tasks
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {tasks_file}. Returning empty list.")
        return [] # Return empty list if file is corrupted or empty
    except Exception as e:
        logger.error(f"An unexpected error occurred loading tasks: {e}")
        return []

def save_tasks(tasks, tasks_file=TASKS_FILE):
    """Saves the current list of tasks to the JSON file."""
    try:
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=4) # Use indent for readability
            logger.debug(f"Tasks saved successfully to {tasks_file}.")
    except IOError as e:
        logger.error(f"Could not write to tasks file {tasks_file}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred saving tasks: {e}")


def add_task(description, priority="normal", tasks_file=TASKS_FILE):
    """Adds a new task to the list."""
    if not description:
        logger.warning("Attempted to add a task with no description.")
        print("Error: Task description cannot be empty.")
        return None

    tasks = load_tasks(tasks_file)

    # Determine the next ID
    if not tasks:
        next_id = 1
    else:
        # Ensure all tasks have 'id' and it's an int, filter out invalid ones
        valid_tasks = [t for t in tasks if isinstance(t.get('id'), int)]
        if not valid_tasks:
             next_id = 1
        else:
            next_id = max(task['id'] for task in valid_tasks) + 1


    new_task = {
        "id": next_id,
        "description": description,
        "priority": priority,
        "status": "pending" # Adding a default status
    }
    tasks.append(new_task)
    save_tasks(tasks, tasks_file)
    logger.info(f"Task added: ID={next_id}, Desc='{description}', Prio='{priority}'")
    return new_task


def list_tasks(tasks_file=TASKS_FILE):
    """Returns the list of all tasks."""
    tasks = load_tasks(tasks_file)
    logger.info(f"Listing {len(tasks)} tasks.")
    return tasks


def delete_task(task_id, tasks_file=TASKS_FILE):
    """Deletes a task by its ID."""
    tasks = load_tasks(tasks_file)
    initial_length = len(tasks)

    # Filter out the task with the matching ID
    # Ensure comparison is between integers
    tasks_to_keep = [task for task in tasks if task.get('id') != task_id]

    if len(tasks_to_keep) == initial_length:
        logger.warning(f"Attempted to delete non-existent task ID: {task_id}")
        return False # Task ID not found
    else:
        save_tasks(tasks_to_keep, tasks_file)
        logger.info(f"Task deleted: ID={task_id}")
        return True # Task successfully deleted
