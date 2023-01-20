import sys

class _AbstractLogger:
    def __init__(self):
        pass

    def __del__(self):
        print ('super.del')             ######################################################
        self.save()

    def __add__(self, o):
        self.log(str(o))
        return self

    def log(self, text: str):
        pass

    def save(self):
        pass
        print ('super.save')            ######################################################

class FileLogger(_AbstractLogger):
    def __init__(self, file):
        super().__init__()
        self.buffer = ''
        self.file = open(file, 'a')

    def __del__(self):
        print ('del')                   ######################################################
        super().__del__()
        self.file.close()

    def log(self, text: str):
        self.buffer += text
        return super().log(text)

    def save(self):
        print ('save')                  ######################################################
        super().save()
        self.file.write(self.log)
        self.buffer = ''

class DebugLogger(_AbstractLogger):
    def log(self, text: str):
        print(text, file=sys.stdout, end='', flush=True)
        return super().log(text)