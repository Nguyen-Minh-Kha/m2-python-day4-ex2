# advanced_cli_task_manager/task_manager/logger.py

import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "task_manager.log")

def setup_logger(log_file=LOG_FILE, log_level=logging.INFO):
    """Sets up the application logger."""

    # Ensure the log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create logger
    logger = logging.getLogger("task_manager")
    logger.setLevel(log_level) # Set the minimum level of messages to handle

    # Prevent adding multiple handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create console handler (optional, for seeing logs in console too)
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(log_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler) # Uncomment to see logs in console

    return logger

# Initialize once
logger = setup_logger()
