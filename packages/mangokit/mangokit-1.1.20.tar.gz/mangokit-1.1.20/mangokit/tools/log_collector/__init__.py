# -*- coding: utf-8 -*-
# @Project: auto_test
# @Description: 
# @Time   : 2023-04-05 12:40
# @Author : 毛鹏
from mangokit.tools.decorator.singleton import singleton
from mangokit.tools.log_collector.log_control import LogHandler


def set_log(log_path):
    log = Log(log_path)
    return log


@singleton
class Log:

    def __init__(self, log_path):
        self.DEBUG = LogHandler(fr"{log_path}\debug-log.log", 'debug')
        self.INFO = LogHandler(fr"{log_path}\info-log.log", 'info')
        self.WARNING = LogHandler(fr"{log_path}\warning-log.log", 'warning')
        self.ERROR = LogHandler(fr"{log_path}\error-log.log", 'error')
        self.CRITICAL = LogHandler(fr"{log_path}\critical-log.log", 'critical')

    def debug(self, msg: str):
        self.DEBUG.logger.debug(str(msg))

    def info(self, msg: str):
        self.INFO.logger.info(str(msg))

    def warning(self, msg: str):
        self.WARNING.logger.warning(str(msg))

    def critical(self, msg: str):
        self.CRITICAL.logger.critical(str(msg))

    def error(self, msg: str):
        self.ERROR.logger.error(str(msg))
