import os
import datetime

MAX_LOG_SIZE = 1 * 1024 * 1024  # 1MB in bytes
NORMAL_LOG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "Blues_Magic_Tarkov_Bot", "normal_log.txt")
ERROR_LOG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "Blues_Magic_Tarkov_Bot", "error_log.txt")

def manage_log_size(file_path):
    """ Manage log size by renaming and creating a new log file when size exceeds MAX_LOG_SIZE. """
    if os.path.exists(file_path) and os.path.getsize(file_path) >= MAX_LOG_SIZE:
        log_backup = file_path + ".old"
        os.rename(file_path, log_backup)  # Rename the old log file
        print(f"Log file {file_path} exceeded size limit. Renamed to {log_backup}.")
        # Create a new empty log file
        open(file_path, 'w').close()

def write_normal_log(message):
    """ Write normal messages to the normal log file, with log size management. """
    try:
        manage_log_size(NORMAL_LOG_FILE)
        with open(NORMAL_LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{message}\n")
    except Exception as e:
        print(f"Error writing to normal log file: {e}")
        write_error_log(f"Error writing to normal log file: {e}")  # Log to error log as well

def write_error_log(message):
    """ Write error messages to the error log file, with timestamp. """
    try:
        manage_log_size(ERROR_LOG_FILE)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{current_time[:10]}][{current_time[11:]}] ERROR: {message}\n")
    except Exception as e:
        print(f"Error writing to error log file: {e}")
        # Further error handling can go here, e.g., sending notifications if critical

