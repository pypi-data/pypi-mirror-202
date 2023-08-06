'''
Logging Configuration

This module provides a basic logging configuration for Python scripts. 
It sets up a logger with the name "codebuddie" and configures it to log 
messages to both a file and the console.

Usage:
    ```python
    import logging
    from codebuddie.logging_module import logger

    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    ```
'''

import logging
import os
import sys

LOGGING_STR = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
LOG_DIR = "./logs"
log_filepath = os.path.join(LOG_DIR, "running_logs.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_STR,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("codebuddie")