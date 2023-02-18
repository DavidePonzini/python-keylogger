import sys
import socket
from datetime import datetime


def get_timestamp():
    return f'\n===== {str(datetime.utcnow())} =====\n'


class AbstractLogger:
    def __init__(self):
        pass

    def close(self) -> None:
        pass

    def log(self, text: str) -> None:
        pass

    def on_attached(self) -> None:
        pass


class FileLogger(AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.file = open(file, 'a')
    
    def on_attached(self) -> None:
        super().on_attached()
        self.write_timestamp()

    def write_timestamp(self) -> None:
        self.file.write(get_timestamp())

    def close(self) -> None:
        super().close()
        self.write_timestamp()
        self.file.write('\n')
        self.file.close()

    def log(self, text: str) -> None:
        super().log(text)
        self.file.write(text)


class ConsoleLogger(AbstractLogger):
    def on_attached(self) -> None:
        super().on_attached()
        print(get_timestamp())

    def close(self) -> None:
        super().close()
        print(get_timestamp())

    def log(self, text: str) -> None:
        super().log(text)
        print(text, file=sys.stdout, end='', flush=True)


class TCPLogger(AbstractLogger):
    def __init__(self, ip, port):
        raise NotImplementedError
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((ip, port))

    def on_attached(self) -> None:
        super().on_attached()
        self.__socket.sendall(get_timestamp())

    def log(self, text: str):
        self.__socket.sendall(text)

    def close(self):
        super().close()
        self.__socket.sendall(get_timestamp())
        self.__socket.close()
