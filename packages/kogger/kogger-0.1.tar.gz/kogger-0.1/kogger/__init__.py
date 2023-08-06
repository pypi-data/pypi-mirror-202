"""
@author: bochengz
@date: 2023/04/11
@email: bochengzeng@bochengz.top
"""
from logger.logger import Logger

default_logger = Logger()


def set_name(name):
    default_logger.name = name


def set_file(file_path):
    default_logger.file = file_path


def info(str):
    default_logger.info(str)


def warning(str):
    default_logger.warning(str)


def error(str):
    default_logger.error(str)
