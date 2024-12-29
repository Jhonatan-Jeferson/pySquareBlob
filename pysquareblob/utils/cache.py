"""This module contains the Cache object"""

import asyncio

from ..data import Account, Object
from .logs import Logger


class Cache:
    """This is the cache object that will be used to store all the cached information"""
    
    __logger = Logger(False)

    def __init__(self, clean_timer: float):
        self.account_info: Account | None = None
        self.objects: list[Object] = []
        self._timer = clean_timer
        self._scheduled = False
        
    def __clean_cache(self):
        """This method cleans the cache"""
        
        self.__logger.info('Clearing all cached info...')
        self.account_info: Account | None = None
        self.objects: list[Object] = []
        self._scheduled = False
        self.schedule_clean()
    
    def schedule_clean(self):
        """This method schedules the cache cleaning"""
        
        if self._scheduled:
            return
        self._scheduled = True
        loop = asyncio.get_event_loop()
        loop.call_later(self._timer, self.__clean_cache)
        