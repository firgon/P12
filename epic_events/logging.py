import logging


class OnlyCustomLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.module == 'middleware'
