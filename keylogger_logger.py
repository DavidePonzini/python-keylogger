import sys
from datetime import datetime


def get_timestamp():
    return f'\n===== {str(datetime.utcnow())} =====\n'


class _AbstractLogger:
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


class FileLogger(_AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.__buffer = ''
        self.file = open(file, 'a')
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

class DebugLogger(_AbstractLogger):
    def on_attached(self):
        super().on_attached()
        print(get_timestamp())

    def close(self):
        super().close()
        print(get_timestamp())

    def log(self, text: str):
        print(text, file=sys.stdout, end='', flush=True)
        return super().log(text)