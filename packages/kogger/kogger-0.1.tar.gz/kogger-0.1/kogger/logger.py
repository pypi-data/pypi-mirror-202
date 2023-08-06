"""
A very simple logger.

@author: bochengz
@date: 2023/04/11
@email: bochengzeng@bochengz.top
"""
from datetime import datetime


class Logger:
    def __init__(self, name=None, file=None):
        self.name = name
        self.file = file

    def str_build(self, tag, str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.name is None:
            return '[{}] [{}] {}'.format(now, tag, str)
        return '[{}] [{}] [{}] {}'.format(now, self.name.upper(), tag, str)

    def info(self, str):
        if self.file is not None:
            with open(self.file, 'a') as f:
                print(self.str_build('INFO', str), file=f)
        else:
            print(self.str_build('INFO', str))

    def warning(self, str):
        if self.file is not None:
            with open(self.file, 'a') as f:
                print(self.str_build('WARNING', str), file=f)
        else:
            print(self.str_build('WARNING', str))

    def error(self, str):
        if self.file is not None:
            with open(self.file, 'a') as f:
                print(self.str_build('ERROR', str), file=f)
        else:
            print(self.str_build('ERROR', str))
