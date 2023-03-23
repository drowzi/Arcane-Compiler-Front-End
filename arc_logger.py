import logging
from constants import DEBUG_MODE, DEBUG_LOG_FILE, LOG_FILE

def get_log_handle(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    if DEBUG_MODE: logger.setLevel(0)
    if DEBUG_LOG_FILE: logger.basicConfig(filename=LOG_FILE)
    return logger