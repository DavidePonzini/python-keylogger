import sys
import socket
from datetime import datetime


def get_timestamp():
    return f'\n===== {str(datetime.utcnow())} =====\n'


class AbstractLogger:
    def __init__(self):
        pass

    def close(self):
        self.save()

    def __add__(self, o):
        self.log(str(o))
        return self

    def log(self, text: str):
        pass

    def save(self):
        pass

    def on_attached(self):
        pass

    def on_detached(self):
        self.save()


class FileLogger(AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.__buffer = ''
        self.file = open(file, 'a')
    
    def on_attached(self):
        self.write_timestamp()

    def write_timestamp(self):
        self.file.write(get_timestamp())

    def close(self):
        super().close()
        self.write_timestamp()
        self.file.write('\n')
        self.file.close()

    def log(self, text: str):
        self.__buffer += text
        return super().log(text)

    def save(self):
        super().save()
        self.file.write(self.__buffer)
        self.__buffer = ''


class ConsoleLogger(AbstractLogger):
    def on_attached(self):
        super().on_attached()
        print(get_timestamp())

    def close(self):
        super().close()
        print(get_timestamp())

    def log(self, text: str):
        print(text, file=sys.stdout, end='', flush=True)
        return super().log(text)


class TCPLogger(AbstractLogger):
    def __init__(self, ip, port):
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((ip, port))

    def log(self, text: str):
        self.__socket.sendall(text)

    def close(self):
        super().close()
        self.__socket.close()