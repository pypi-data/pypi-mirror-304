import logging
import logging.handlers
import sys
import os

# Determine the log file directory
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)


# Logging configuration
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Set the root logger level

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler for logging to stdout/stderr
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Customize the console level if needed
    console_handler.setFormatter(formatter)

    # File handler for logging to a file
    log_file = os.path.join(log_dir, 'app.log')  # Customize log file name
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024 * 1024 * 5, backupCount=5
    )  # 5 MB log file with 5 rotations
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
