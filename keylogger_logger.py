import sys
from datetime import datetime


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

class FileLogger(_AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.buffer = ''
        self.file = open(file, 'a')
        self.write_timestamp()

    def write_timestamp(self):
        self.file.write(f'\n===== {str(datetime.utcnow())} =====\n')

    def close(self):
        super().close()
        self.write_timestamp()
        self.file.write('\n')
        self.file.close()

    def log(self, text: str):
        self.buffer += text
        return super().log(text)

    def save(self):
        super().save()
        self.file.write(self.buffer)
        self.buffer = ''

class DebugLogger(_AbstractLogger):
    def log(self, text: str):
        print(text, file=sys.stdout, end='', flush=True)
        return super().log(text)