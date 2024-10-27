# spicy_ids/utils/logger.py

from loggerLogs import CustomLogger

LOG_LEVEL: int = 20


logger: CustomLogger = CustomLogger(
    log_level=20,
    console_log=True,
    console_log_level=20,
    file_log=False,
)
