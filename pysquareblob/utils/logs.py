"""This module contains the Logger implementation"""

from datetime import datetime

class Logger:
    """This class implements a log handler"""
    
    STD_OUT_STR = '{time} - {color}[{level}] {message}\033[0m'
    LOGGER: 'Logger' = None
    
    def __init__(self, debug: bool) -> None:
        self.debug = debug
        
    def __new__(cls, *args, **kwargs) -> 'Logger':
        if not cls.LOGGER:
            cls.LOGGER = super().__new__(cls)
        return cls.LOGGER
    
    def _colorize(self, color: str) -> str:
        """Returns the color code for the terminal"""
            
        colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'white': '\033[97m',
        }
        return colors.get(color)
    
    def _get_time(self) -> str:
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
    def info(self, text: str) -> None:
        """Prints an info log message"""
        
        if self.debug:
            print(
                self.STD_OUT_STR.format(
                time=self._get_time(),
                color=self._colorize('blue'),
                level='INFO',
                message=text
            ))    
        
    def warning(self, text: str) -> None:
        """Sends a warning log message"""
        
        if self.debug:
            print(
                self.STD_OUT_STR.format(
                    time=self._get_time(),
                    color=self._colorize('yellow'),
                    level='WARNING',
                    message=text
                )
            )
            
    def error(self, text: str, error: Exception) -> None:
        """Sends a error log message and raises it"""
        
        print(
            self.STD_OUT_STR.format(
                time=self._get_time(),
                color=self._colorize('red'),
                level='ERROR',
                message=f'{text}'
            )
        )
        raise error