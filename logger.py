import sys
import socket
from datetime import datetime
from abc import ABC, abstractclassmethod

def get_timestamp():
    return f'\n===== {str(datetime.utcnow())} =====\n'


class AbstractLogger(ABC):
    def __init__(self):
        pass

    def close(self) -> None:
        self.log(get_timestamp())
        self.log('\n')

    @abstractclassmethod
    def log(self, text: str) -> None:
        pass

    def on_attached(self) -> None:
        self.log(get_timestamp())


class FileLogger(AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.file = open(file, 'a')
    
    def close(self) -> None:
        super().close()
        self.file.close()

    def log(self, text: str) -> None:
        super().log(text)
        self.file.write(text)


class ConsoleLogger(AbstractLogger):
    def close(self) -> None:
        super().close()

    def log(self, text: str) -> None:
        super().log(text)
        print(text, file=sys.stdout, end='', flush=True)


class TCPLogger(AbstractLogger):
    def __init__(self, ip, port):
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((ip, port))

    def log(self, text: str):
        super().log(text)
        self.__socket.sendall(text.encode())

    def close(self):
        super().close()
        self.__socket.close()
