# advanced_cli_task_manager/tests/test_core.py

import unittest
import os
import json
import sys

# Add the project root to the Python path to allow importing 'task_manager'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now import from task_manager. Needs to happen *after* path modification
from task_manager.core import add_task, list_tasks, delete_task, load_tasks, save_tasks
from task_manager.config import TASKS_FILE # Import to know the default if needed

# Define a specific file for testing
TEST_TASKS_FILE = os.path.join(os.path.dirname(__file__), "test_tasks.json")

class TestTaskManagerCore(unittest.TestCase):

    def setUp(self):
        """Set up a clean state before each test."""
        # Ensure the test file does not exist before a test
        if os.path.exists(TEST_TASKS_FILE):
            os.remove(TEST_TASKS_FILE)
        # Create an empty test file for some tests if needed
        # save_tasks([], tasks_file=TEST_TASKS_FILE)
        # Or simply let load_tasks handle non-existence

    def tearDown(self):
        """Clean up after each test."""
        # Remove the test file after a test runs
        if os.path.exists(TEST_TASKS_FILE):
            os.remove(TEST_TASKS_FILE)

    def test_load_tasks_file_not_found(self):
        """Test loading tasks when the file doesn't exist."""
        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(tasks, [])

    def test_load_tasks_empty_file(self):
        """Test loading tasks from an empty or invalid JSON file."""
        with open(TEST_TASKS_FILE, 'w') as f:
            f.write("") # Empty file
        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(tasks, [])

        with open(TEST_TASKS_FILE, 'w') as f:
            f.write("invalid json") # Invalid JSON
        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(tasks, [])

    def test_add_task(self):
        """Test adding a single task."""
        description = "Test Task 1"
        priority = "high"
        added_task = add_task(description, priority, tasks_file=TEST_TASKS_FILE)

        self.assertIsNotNone(added_task)
        self.assertEqual(added_task['description'], description)
        self.assertEqual(added_task['priority'], priority)
        self.assertEqual(added_task['id'], 1) # First task should have ID 1
        self.assertEqual(added_task['status'], 'pending')

        # Verify by loading tasks directly
        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], description)

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks and ID assignment."""
        add_task("Task A", "low", tasks_file=TEST_TASKS_FILE)
        add_task("Task B", "normal", tasks_file=TEST_TASKS_FILE)
        added_task_c = add_task("Task C", "high", tasks_file=TEST_TASKS_FILE)

        self.assertEqual(added_task_c['id'], 3) # Should be the third task

        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(len(tasks), 3)
        # Check if IDs are unique and sequential (in this simple case)
        ids = {task['id'] for task in tasks}
        self.assertEqual(ids, {1, 2, 3})

    def test_list_tasks(self):
        """Test listing tasks."""
        # Test with no tasks
        tasks = list_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(tasks, [])

        # Add some tasks
        add_task("List Task 1", tasks_file=TEST_TASKS_FILE)
        add_task("List Task 2", tasks_file=TEST_TASKS_FILE)

        tasks = list_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['description'], "List Task 1")
        self.assertEqual(tasks[1]['description'], "List Task 2")

    def test_delete_task_exists(self):
        """Test deleting an existing task."""
        add_task("Delete Me", "low", tasks_file=TEST_TASKS_FILE) # ID 1
        add_task("Keep Me", "high", tasks_file=TEST_TASKS_FILE)  # ID 2

        result = delete_task(1, tasks_file=TEST_TASKS_FILE)
        self.assertTrue(result) # Deletion should be successful

        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], "Keep Me")
        self.assertEqual(tasks[0]['id'], 2) # Check remaining task ID

    def test_delete_task_not_exists(self):
        """Test deleting a non-existent task."""
        add_task("Existing Task", "normal", tasks_file=TEST_TASKS_FILE) # ID 1

        result = delete_task(99, tasks_file=TEST_TASKS_FILE) # Try deleting non-existent ID
        self.assertFalse(result) # Deletion should fail

        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(len(tasks), 1) # List should be unchanged
        self.assertEqual(tasks[0]['id'], 1)

    def test_delete_only_task(self):
        """Test deleting the only task."""
        add_task("Only Task", "normal", tasks_file=TEST_TASKS_FILE) # ID 1
        result = delete_task(1, tasks_file=TEST_TASKS_FILE)
        self.assertTrue(result)
        tasks = load_tasks(tasks_file=TEST_TASKS_FILE)
        self.assertEqual(len(tasks), 0) # List should be empty


if __name__ == "__main__":
    unittest.main()
