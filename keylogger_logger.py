import sys

class _AbstractLogger:
    def __init__(self):
        pass

    def __del__(self):
        self.save()

    def __add__(self, o):
        self.log(str(o))
        return self

    def log(self, text: str):
        return self

    def save(self):
        pass

class FileLogger(_AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.log = ''
        self.file = open(file, 'a')

    def __del__(self):
        super().__del__()
        self.file.close()

    def log(self, text: str):
        self.log += text
        return super().log(text)

    def save(self):
        super().save()
        self.file.write(self.log)
        self.log = ''

class DebugLogger(_AbstractLogger):
    def log(self, text: str):
        print(text, file=sys.stdout, end='', flush=True)
        return super().log(text)