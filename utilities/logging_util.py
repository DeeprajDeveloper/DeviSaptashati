import logging
from datetime import datetime
import inspect

# Configure logging
logging.basicConfig(format='[%(levelname)s] [%(asctime)s] - %(message)s', level=logging.INFO)


def log_message(level, message, call_type):
    """
    Logs a message with the function name dynamically.
    OPTIONS: info/error/debug/warning
    """
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    function_name = inspect.currentframe().f_back.f_code.co_name
    full_message = f"[{call_type}] {function_name}(): {message}"
    if level == "info":
        logging.info(full_message)
    elif level == "error":
        logging.error(full_message)
    elif level == "debug":
        logging.debug(full_message)
    elif level == "warning":
        logging.warning(full_message)
    else:
        logging.info(full_message)

    with open(const.DEFAULT_LOG_FILE, 'a', encoding='utf-8') as logfile_obj:
        logfile_obj.write(f"[{current_date}][{level}] - {full_message}\n")
